# pylint: disable=missing-function-docstring

"""
### ETL DAG Tutorial Documentation
This ETL DAG is compatible with Airflow 1.10.x (specifically tested with 1.10.12) and is referenced
as part of the documentation that goes along with the Airflow Functional DAG tutorial located
[here](https://airflow.apache.org/tutorial_decorated_flows.html)
"""
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

with DAG(
    'test_tasks',
    default_args=default_args,
    description='ETL DAG Test',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['test'],
) as dag:
    dag.doc_md = __doc__

    # [START extract_function]
    def extract(**kwargs):
        ti = kwargs['ti']
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        ti.xcom_push('order_data', data_string)

    # [END extract_function]

    # [START transform_function]
    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push('total_order_value', total_value_json_string)

    # [END transform_function]

    # [START load_function]
    def load(**kwargs):
        ti = kwargs['ti']
        total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
        total_order_value = json.loads(total_value_string)

        print(total_order_value)

    # [END load_function]

    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = """\
#### Extract task
A simple Extract task to get data ready for the rest of the data pipeline.
In this case, getting data is simulated by reading from a hardcoded JSON string.
This data is then put into xcom, so that it can be processed by the next task.
"""

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = """\
#### Transform task
A simple Transform task which takes in the collection of order data from xcom
and computes the total order value.
This computed value is then put into xcom, so that it can be processed by the next task.
"""

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    load_task.doc_md = """\
#### Load task
A simple Load task which takes in the result of the Transform task, by reading it
from xcom and instead of saving it to end user review, just prints it out.
"""

    extract_task >> transform_task >> load_task
