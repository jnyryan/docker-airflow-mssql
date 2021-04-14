#!/usr/bin/env bash
mkdir -p ./dags ./logs ./plugins ./data
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
echo -e "AIRFLOW_IMAGE_NAME=search/apache:2.0.1" >> .env
docker-compose up airflow-init
