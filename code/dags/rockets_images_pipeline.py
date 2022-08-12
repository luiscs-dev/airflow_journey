from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import json
import pathlib
import requests
import requests.exceptions as requests_exceptions

LAUNCHES_FILE = "/tmp/launches.json"
IMG_DIR = "/tmp/images"

doc_md = """
### Data Pipelines with Apache Airflow

This code was learnt while reading this amazing book.
I did some slight changes to the code but the idea was explained in the book.

- [You can find the book here](https://example.com/)
"""

def _get_pictures():
    pathlib.Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

    with open(LAUNCHES_FILE) as f:
        launches = json.load(f)
        image_urls = [ launch["image"] for launch in launches["results"]]

        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"{IMG_DIR}/{image_filename}"

                with open(target_file, "wb") as f:
                    f.write(response.content)

                print(f"Downloaded {image_url} to {target_file}")
            except requests_execptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")


with DAG(dag_id = "download_rokect_launches", start_date = days_ago(1), schedule_interval = None, doc_md=doc_md) as dag:
    download_launches = BashOperator(task_id = "download_launches",
            bash_command=f"curl -o {LAUNCHES_FILE} -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'")

    get_pictures = PythonOperator(task_id = "get_pictures",
            python_callable=_get_pictures)

    notify = BashOperator(task_id = "notify", 
            bash_command = f'echo "There are now $(ls {IMG_DIR} | wc -l) images."')

    download_launches >> get_pictures >> notify


