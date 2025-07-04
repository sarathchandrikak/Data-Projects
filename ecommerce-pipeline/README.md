
# 🧩 Problem Statement
The goal of this project is to build a data ingestion and transformation pipeline that:

-> Ingests raw data automatically from a Google Cloud Storage (GCS) bucket into a raw table in BigQuery
-> Performs data transformations and writes the results into a modified (cleaned or modeled) BigQuery table
-> Orchestrates and schedules these steps using Astronomer Airflow DAGs, ensuring reliability and visibility
-> (Optional enhancement) Incorporates a Cloud Run service that is triggered when new files are added to the GCS bucket, enabling near real-time ingestion and transformation

### 🧩 Business Use Case

To provide real-time updates on the latest YouTube metrics for user playlists, ensuring accurate and timely visibility into views, likes, and comments.

### 🧩 Stages of Pipeline

| Component              | Benefit                                   |
| ---------------------- | --------------------------------------------------- |
| **Raw GCS → BQ Table** | Centralizes all raw user event data                 |
| **DataProc Serverless**| Business logic to do transformations and add data transformed data to BQ table    |
| **Airflow DAGs**       | Ensures DAGS run and add data to BQ tables          |
| **Cloud Run Trigger**  | Enables near real-time ingestion for fresh insights |


### 🧩 Architecture Diagram

![Image](https://github.com/sarathchandrikak/Data-Projects/blob/main/ecommerce-pipeline/etl-pipeline.png)

### 🧩 Files Description

bq_ddl_commands.sql -> SQL commands to create tables in bigquery\
transform_join_ecommerce.py -> PySpark code that transforms raw data and writes into bigquery table
ecommerce_data_pipeline_dag.py -> Python DAGs that initially loads data into tables followed by Dataproc serverless job invocation to run the pyspark script
requirements.txt -> Requirements needed to run the astronomer airflow job

### 🧩 Commands to Run

      brew install astro -> To install astronomer
      mkdir <your-astro-project-name> -> To create astronomer project
      cd <your-astro-project-name> -> To change pwd
      astro dev init -> To initialise astronomer project
      astro login astronomer.io -> To login to astronomer
      astro deploy --dags -> To deploy dags in astronomer 

