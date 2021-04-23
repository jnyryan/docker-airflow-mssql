#!/usr/bin/env bash
mkdir -p ./dags ./logs ./plugins ./data
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
echo -e "AIRFLOW_IMAGE_NAME=search/apache:2.0.1" >> .env
#echo -e "AIRFLOW_CONN_TEST_DB=mssql+pyodbc://sa:Iamnotsecure4sure@localhost:1433/TEST_DB?driver=ODBC+Driver+17+for+SQL+Server" >> .env
echo -e "AIRFLOW_CONN_TEST_DB=mssql://sa:Iamnotsecure4sure@localhost:1433/TEST_DB" >> .env

# set up SOLR
mkdir -p ./data/solr_home
cp ./etc/solr/* ./data/solr86/solr_home

docker-compose up airflow-init
