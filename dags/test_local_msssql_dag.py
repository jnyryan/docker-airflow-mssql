from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context, task
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

with DAG(
    'test_local_msssql_dag',
    default_args=default_args,
    description='test local mssql dag',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['test'],
) as dag:
    dag.doc_md = __doc__

    def start(**kwargs):
        print("MEH!")

    def extract(**kwargs):
        conn = MsSqlHook.get_connection(conn_id="mssql_test_db")
        hook = conn.get_hook()
        df = hook.get_pandas_df(sql="SELECT top 5 * FROM DRUGS")
        #do whatever you need on the df
        print(df)

    start_task = PythonOperator(
        task_id='start',
        python_callable=start,
    )

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    start_task >> extract_task