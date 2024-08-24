import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="mlflow-ray-serve",
    version="0.5.0",
    description="Ray Serve MLflow deployment plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ray-project/mlflow-ray-serve",
    packages=setuptools.find_packages(),
    #install_requires=["ray[serve]", "mlflow"],
    entry_points={"mlflow.deployments": "ray-serve=mlflow_ray_serve"},
    license="Apache 2.0")
