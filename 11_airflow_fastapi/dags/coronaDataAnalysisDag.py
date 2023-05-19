from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

import sys, os

from MLprocess.CoronaDataMain import *

coronaData = CoronaDataMain()


def print_result(**kwargs):
    r = kwargs["task_instance"].xcom_pull(key='result_msg')
    print("message : ", r)


default_args = {
    'owner': 'owner-name',
    'depends_on_past': False,
    'email': ['your-email@g.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

dag_args = dict(
    dag_id="tutorial-ml-op",
    default_args=default_args,
    description='tutorial DAG ml',
    schedule_interval=timedelta(minutes=50),
    start_date=datetime(2022, 2, 1),
    tags=['example-sj'],
)

with DAG(**dag_args) as dag:
    start = BashOperator(
        task_id='start',
        bash_command='echo "start!"',
    )

    loaddata_task = PythonOperator(
        task_id='save_excel_from_url',
        python_callable=coronaData.save_excel_from_url(),
        op_kwargs={}
    )

    prepro_task = PythonOperator(
        task_id='preprocessing',
        python_callable=coronaData.preprocess_data(),
        op_kwargs={}
    )

    prepro_task = PythonOperator(
        task_id='check_feature',
        python_callable=coronaData.visualize()
        op_kwargs={}
    )

    modeling_task = PythonOperator(
        task_id='modeling',
        python_callable=titanic.run_modeling,
        op_kwargs={'n_estimator': 100, 'flag': True}
    )

    msg = PythonOperator(
        task_id='msg',
        python_callable=print_result
    )

    complete = BashOperator(
        task_id='complete_bash',
        bash_command='echo "complete~!"',
    )

    start >> prepro_task >> modeling_task >> msg >> complete
