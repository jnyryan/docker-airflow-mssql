#!/usr/bin/env bash
echo '***********************************************************'
echo 'building custom airflow'
echo '***********************************************************'
docker build -t search/apache:2.0.1 -f ./etc/Dockerfile .
