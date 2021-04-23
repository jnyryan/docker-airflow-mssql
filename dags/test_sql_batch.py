from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context, task
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.utils.dates import days_ago
from lib.TestData import TestData

default_args = {
    'owner': 'airflow',
}

with DAG(
    'test_sql_batch',
    default_args=default_args,
    description='test sql batch',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['test'],
) as dag:
    dag.doc_md = __doc__

    def start(**kwargs):
        print("MEH!")

    def extract(**kwargs):
        data = TestData().get_batched_data()
        ti = kwargs['ti']
        ti.xcom_push('data', data)

    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data = ti.xcom_pull(task_ids='extract', key='data')
        print("some transform")
        print(extract_data)

## Task Definitions

    start_task = PythonOperator(
        task_id='start',
        python_callable=start,
    )

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    start_task >> extract_task >> transform_task