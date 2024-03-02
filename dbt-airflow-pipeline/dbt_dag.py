import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG with the specified schedule interval
dag = DAG('dbt_dag', default_args=default_args, schedule_interval=timedelta(days=1))

# Define dbt commands as BashOperators
dbt_commands = [
    "dbt run"
]

for dbt_command in dbt_commands:
    task_id = dbt_command.replace(" ", "_")  # Convert spaces to underscores for task_id
    dbt_task = BashOperator(
        task_id=task_id,
        bash_command=f"cd /Users/sarathchandrika/airflow/dags/dbt/etl_pipeline && {dbt_command}",
        dag=dag
    )

    # Chain tasks
    dbt_task