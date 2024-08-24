
# MLflow Docker - MLflow Tracking Server and PostgreSQL 

## Overview

Launches a full-fledged MLflow server environment consisting of two containers:
* mlflow_server - MLflow tracking server
* mlflow_postgresql - PostgreSQL database server

Two types of mlflow_server containers can be built depending on where the artifact repository lives:
  * local - mounted shared volume between (laptop) host and container 
  * S3 - artifacts are stored on S3

See [MLflow Tracking Servers](https://mlflow.org/docs/latest/tracking.html#mlflow-tracking-servers) and
[Referencing Artifacts](https://mlflow.org/docs/latest/concepts.html#referencing-artifacts).


## Run
I. lunch minio as s3 server

```
docker-compose -f docker-compose-minio.yaml up

```
- go to 127.0.01:9001  (user/pass: minioadmin/minioadmin)
| create (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY) and bucket for next step
   
  

II. Lunch MLflow

The required  environment variables are specified in the standard docker compose `.env` file.
Copy one of the two `.env` template files to `.env`, make appropriate changes and then run docker-compose.

To launch a local MLflow server:
```
change .env **** base on .env-local-template
docker-compose -f docker-compose.yaml -f docker-compose-local.yaml  up -d 
```

To launch an S3 MLflow server:
```
change .env ***** base on .env-s3-template
docker-compose -f docker-compose.yaml -f docker-compose-s3.yaml up -d 
```
You will then see two containers:
```
CONTAINER ID  IMAGE                  COMMAND                  PORTS                     NAMES
7a4be1019858  mlflow_server:latest   "/bin/sh -c 'cd /hom…"   0.0.0.0:5005->5000/tcp    mlflow_server
3b4eb5a2026e  mlflow_postgres:16.4    "docker-entrypoint.s…"   0.0.0.0:5432->5432/tcp   mlflow_postgres
```
If you don't see the `mlflow_server` container, just run the docker-compose command again. 
It failed to start because `mlflow_postgres` wasn't up yet. It's a TODO to add a wait-until-alive feature.

## Environment variables

| Env Var  | Description  | Default  |
|:--|:--|:--|
| **PostgreSQL**  |   |   |
| POSTGRES_USER | PostgreSQL postgres password  | efcodd   |
| HOST_POSTGRES_PORT  | Port exposed on host  | 5306  |
|  HOST_POSTGRES_DATA_DIR  | Host mounted volume path |   |
| **MLflow**  |   |   |
| MLFLOW_ARTIFACT_URI  | Base URI for artifacts - either S3 or local path|   |
| HOST_MLFLOW_PORT  | Port exposed on host for tracking server  | 5005  |
| **MLflow S3**  |   |   |
| AWS_ACCESS_KEY_ID  |   |   |
| AWS_SECRET_ACCESS_KEY  |   |   |


**Sample local .env**
```
# PostgreSQL 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=efcodd
HOST_POSTGRES_PORT=5306
HOST_POSTGRES_DATA_DIR=/opt/mlflow_docker/postgres

# MLflow tracking server
MLFLOW_ARTIFACT_URI=/opt/mlflow_docker/mlflow_server
HOST_MLFLOW_PORT=5005
```

**Sample S3 .env**
```
# PostgreSQL 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=efcodd
HOST_POSTGRES_PORT=5306
HOST_POSTGRES_DATA_DIR=/opt/mlflow_docker/postgres

# MLflow tracking server
MLFLOW_ARTIFACT_URI=s3://my-bucket/mlflow
HOST_MLFLOW_PORT=5005

# AWS 
AWS_ACCESS_KEY_ID=my_access_key_id
AWS_SECRET_ACCESS_KEY=my_secret_access_key
```


## Login to containers

You can check things out inside the containers.
```
docker exec -i -t mlflow_server /bin/bash
```
```
docker exec -i -t mlflow_postgres /bin/bash
```
## The sample output of MLflow 
![plot](./figs/output_example.png)

## The result of MLflow Authentication
![plot](./figs/auth_result.png)

