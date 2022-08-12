# Airflow Journey Notes

Repo to keep notes regarding my airflow learning journey.

## Airflow DAG vocabulary
> A DAG is responsable for orchestrate the execution of a collection of operators.

**dag_id** is the name of the DAG displayed in the Airflow UI
**start_date** is the datetime in which the workflow should start running

### Operators
> An operator performs a single unit of work, runs independly of other operators.

Dependendies between operators is set by '>>'. 

Some examples of operators are:
- BashOperator
- PythonOperator


## Install Airflow locally
Airflow three core components are:
- a scheduler
- a webserver
- a database

### Airflow with PIP install 
Install the python package.
`pip install apache-airflow`

Initialize the metastore.
`airflow db init`
`airflow users create --username admin --password admin`

Copy dags.
`cp <dag_file>.py ~/airflow/dags`

Start webserver and scheduler
`airflow webserver`
`airflow scheduler`

### Airflow with Docker
```bash
docker run \
-ti \
-p 8080:8080 \
-v ./code/dags:/opt/airflow/dags \
--entrypoint=/bin/bash \
--name airflow \
apache/airflow:2.0.0-python3.8 \
-c '( \
  airflow db init && \
  airflow users create \
          --username admin \
          --password admin \
          --firstname FIRST_NAME \
          --lastname LAST_NAME \
          --role Admin \
          --email admin@example.org
); \
airflow webserver & airflow scheduler'

```


