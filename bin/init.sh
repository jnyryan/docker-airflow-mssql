#!/usr/bin/env bash
mkdir -p ./dags ./logs ./plugins ./data
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
echo -e "AIRFLOW_IMAGE_NAME=search/apache:2.0.1" >> .env
#echo -e "AIRFLOW_CONN_TEST_DB=mssql+pyodbc://sa:Iamnotsecure4sure@sql-server-db:1433/TEST_DB?driver=ODBC+Driver+17+for+SQL+Server" >> .env
echo -e "AIRFLOW_CONN_TEST_DB=mssql://sa:Iamnotsecure4sure@sql-server-db:1433/TEST_DB" >> .env

# set up SOLR
mkdir -p ./data/solr ./data/solr/data
cp ./etc/solr/* ./data/solr/data

docker-compose up airflow-init
