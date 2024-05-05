# Online Retail Data Pipeline


# Data Orchestration

Data Orchestration is the coordination and automation of data flow across various tools and systems to deliver quality data products and analytics.\
The path to modern data orchestration solutions like Airflow had various evolutions starting with basic time-based scheduling tools (e.g., Cron, WTS), followed by proprietary software (e.g., AutoSys, Informatica), and finally older open-source solutions (e.g., Oozie, Luigi).


# Airflow 

Apache Airflow is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. It's main components are

* DAG: A directed acyclical graph that represents a single data pipeline
* Task: An individual unit of work in a DAG
* Operator: The specific work that a Task performs 

There are three main types of operators:
  * Action: Perform a specific action such as running code or a bash command
  * Transfer: Perform transfer operations that move data between two systems
  * Sensor: Wait for a specific condition to be met (e.g., waiting for a file to be present) before running the next task
