import logging
from typing import Optional

import mlflow.pyfunc
import pandas as pd
import ray
from mlflow.deployments import BaseDeploymentClient
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE
from ray import serve
from starlette.requests import Request
from ray.runtime_env import RuntimeEnv
# from ray.serve.handle import DeploymentHandle, DeploymentResponse


try:
    import ujson as json
except ModuleNotFoundError:
    import json

logger = logging.getLogger(__name__)

import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



def target_help():
    # TODO: Improve
    help_string = (
        "The mlflow-ray-serve plugin integrates Ray Serve "
        "with the MLFlow deployments API.\n\n"
        "Before using this plugin, you must set up a "
        "detached Ray Serve instance running on "
        "a long-running Ray cluster. "
        "One way to do this is to run `ray start --head` followed by "
        "`serve start`.\n\n"
        "Basic usage:\n\n"
        "    mlflow deployments <command> -t ray-serve\n\n"
        "For more details and examples, see the README at "
        "https://github.com/ray-project/mlflow-ray-serve"
        "/blob/master/README.md"
    )
    return help_string


def run_local(name, model_uri, flavor=None, config=None):
    # TODO: implement
    raise MlflowException("mlflow-ray-serve does not currently " "support run_local.")


@serve.deployment
class MLflowDeployment:
    def __init__(self, model_uri):
        import os 
        remote_server_uri = os.getenv('MLFLOW_TRACKING_URI')
        if remote_server_uri is None:
            raise Exception("you need to set MLFLOW_TRACKING_URI env")
        mlflow.set_tracking_uri(remote_server_uri)
        self.model = mlflow.pyfunc.load_model(model_uri=model_uri)

    async def predict(self, df):
        return self.model.predict(df) #json.dumps(self.model.predict(df), cls=NumpyEncoder)
        
    async def _process_request_data(self, request: Request) -> pd.DataFrame:
        if isinstance(request, pd.DataFrame):
            return request
        body = await request.body()
        if isinstance(body, pd.DataFrame):
            return body
        jbody = json.loads(body)
        if "schema" in jbody:
            schema = json.loads(jbody["schema"])
            df = pd.DataFrame(json.loads(jbody["dataframe"])).astype(schema)
        else:
            df = pd.DataFrame(json.loads(jbody["dataframe"]))
        return df

    async def __call__(self, request: Request):
        df = await self._process_request_data(request)
        return self.model.predict(df)# json.dumps(self.model.predict(df), cls=NumpyEncoder)

class RayServePlugin(BaseDeploymentClient):
    def __init__(self, uri):
        super().__init__(uri)
        import os
        runtime_env = RuntimeEnv(
            env_vars={
                
                      "MLFLOW_S3_ENDPOINT_URL": os.getenv('MLFLOW_S3_ENDPOINT_URL'),
                      "MLFLOW_TRACKING_URI": os.getenv('MLFLOW_TRACKING_URI'), 
                      "MLFLOW_TRACKING_USERNAME": os.getenv('MLFLOW_TRACKING_USERNAME'),
                      "MLFLOW_TRACKING_PASSWORD": os.getenv('MLFLOW_TRACKING_PASSWORD'),
                      "RAY_API_ENDPOINT_URL": os.getenv("RAY_API_ENDPOINT_URL"),
                      "AWS_ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID'),
                      "AWS_SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY')
                     
            }
        )
        try:
            address = self._parse_ray_server_uri(uri)
            if address is not None:
                ray.init(address, namespace="serve", runtime_env=runtime_env)  # Ray Client connection 
            else:
                ray.init(address="auto", namespace="serve", runtime_env=runtime_env)

        except ConnectionError:
            raise MlflowException("Could not find a running Ray instance.")
        # try:
        #     self.client = serve.connect()
        # except RayServeException:
        #     raise MlflowException(
        #         "Could not find a running Ray Serve instance on this Ray " "cluster."
        #     )

    def help(self):
        return target_help()

    def create_deployment(self, name, model_uri, flavor=None, config=None):
        if flavor is not None and flavor != "python_function":
            raise MlflowException(
                message=(
                    f"Flavor {flavor} specified, but only the python_function "
                    f"flavor is supported by mlflow-ray-serve."
                ),
                error_code=INVALID_PARAMETER_VALUE,
            )
        if config is None:
            config = {}
        
        app = MLflowDeployment.options(name=name, **config).bind(model_uri)
        serve.run(app, name=name, route_prefix="/" + name)
        
        # self.client.create_backend(name, MLflowDeployment, model_uri, config=config)
        # self.client.create_endpoint(
        #     name, backend=name, route=("/" + name), methods=["GET", "POST"]
        # )
        
        return {"name": name, "config": config, "flavor": "python_function"}

    def delete_deployment(self, name):
        if any(name == d["name"] for d in self.list_deployments()):
            ray.serve.delete(name)
        # self.client.delete_endpoint(name)
        # self.client.delete_backend(name)
            logger.info("Deleted model with name: {}".format(name))
        logger.info("Model with name {} does not exist.".format(name))

    def update_deployment(self, name, model_uri=None, flavor=None, config=None):
        if model_uri is None:
            raise Exception("you need to set model_uri, flavor, config")
        else:
            self.delete_deployment(name)
            self.create_deployment(name, model_uri, flavor, config)
        return {"name": name, "config": config, "flavor": "python_function"}

    def list_deployments(self, **kwargs):
        r = [{"name": name, "info": info} for name, info in serve.status().applications.items()] 
        
        return r
        

    def get_deployment(self, name):
        try:
            return {"name": name, "info": serve.status().applications[name]}
        except KeyError:
            raise MlflowException(f"No deployment with name {name} found")

    def predict(self, deployment_name, df):
        # File name: composed_client.py
        import requests
        import json
        body = {
            "dataframe": df.to_json(orient="records"),
             "schema": json.dumps(df.dtypes.to_dict(), default=str)
            
        }
        response = requests.post(self.get_endpoint(deployment_name), json=body)
        return response.text

    def get_endpoint(self, deployment_name):
        import os
        return f"{os.getenv('RAY_API_ENDPOINT_URL')}/{deployment_name}"

        

    @staticmethod
    def _parse_ray_server_uri(uri: str) -> Optional[str]:
        """
        Uri accepts password and host/port

        Examples:
        >> ray-serve://my-host:10001
        """
        prefix = "ray-serve://"
        if not uri.startswith(prefix):
            return None
        address = "ray://" + uri[len(prefix):]
        return address
