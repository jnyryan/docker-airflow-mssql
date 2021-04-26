from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context, task
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.utils.dates import days_ago
from importers.BasicSQL2SolrImport import BasicSQL2SolrImport
import requests
import json

default_args = {
    'owner': 'airflow',
}

with DAG(
    'basic_sql2solr_etl_dag',
    default_args=default_args,
    description='basic import sql data to solr',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['test'],
) as dag:
    dag.doc_md = __doc__

    def extract(**kwargs):
        print("*** EXTRACT")
        extract_data = BasicSQL2SolrImport().extract()
        return extract_data

    def transform(**kwargs):
        print("*** TRANSFORM")
        ti = kwargs['ti']
        extract_data = ti.xcom_pull(task_ids='extract')
        transform_data = BasicSQL2SolrImport().transform(extract_data)
        return transform_data

    def load(**kwargs):
        print("*** LOAD")
        ti = kwargs['ti']
        transform_data = ti.xcom_pull(task_ids='transform')
        load_data = BasicSQL2SolrImport().load(transform_data)
        print(load_data)
        return load_data

    def report(**kwargs):
        print("*** REPORT")
        ti = kwargs['ti']
        load_data = ti.xcom_pull(task_ids='load')
        print(load_data)


## Task Definitions

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    report_task = PythonOperator(
        task_id='report',
        python_callable=report,
    )

    extract_task >> transform_task >> load_task >> report_task
