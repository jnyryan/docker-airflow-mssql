# Docker Airflow Tutorial

Airflow setup to hit a SQL Server database

Reference: https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#

## Usage

```
make init
make build
make start
```

## SQL Server

Run a local SQL Server to play with.

Refernce: https://hub.docker.com/_/microsoft-mssql-server

``` bash

docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=Iamnotsecure4sure' -e 'MSSQL_PID=Express' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2017-latest-ubuntu

docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=Iamnotsecure4sure' --name 'sql-2019' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest`.

```

## SOLR

Run a local SOLR instance to put the ETL data into

username: solr
password: SolrRocks