from airflow.decorators import dag, task
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from pendulum import datetime
import uuid
from airflow.operators.bash import BashOperator

@dag(
    dag_id="gcs_to_bq_dataproc_ecommerce",
    description=(
        "Load products & orders JSON from GCS into BigQuery (overwrite), "
        "then run a Dataproc Serverless PySpark batch to transform/join "
        "and append to enriched_orders."
    ),
    start_date=datetime(2025, 7, 3),
    schedule=None,
    catchup=False,
    tags=["astronomer", "gcs", "bigquery", "dataproc", "ecommerce"],
)
def gcs_to_bq_dataproc_ecommerce():

    project_id = "{{ var.value.gcp_project_id }}"
    dataset   = "retail_data"      
    bucket    = "datasets-ecommerce"
    temp_bucket = "bq-tmp-dat"    

    # 1) Overwrite-load products.json → retail_data.products
    load_products = GCSToBigQueryOperator(
        task_id="load_products",
        gcp_conn_id="gcp_conn",
        bucket=bucket,
        source_objects=["datasets/products/products.json"],
        destination_project_dataset_table=f"{project_id}.{dataset}.products",
        source_format="NEWLINE_DELIMITED_JSON",
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
        location="US",
    )

    # 2) Overwrite-load orders.json → retail_data.orders
    load_orders = GCSToBigQueryOperator(
        task_id="load_orders",
        gcp_conn_id="gcp_conn",
        bucket=bucket,
        source_objects=["datasets/orders/orders.json"],
        destination_project_dataset_table=f"{project_id}.{dataset}.orders",
        source_format="NEWLINE_DELIMITED_JSON",
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
        location="US",
    )

    batch_id = f"ecom-transform-{str(uuid.uuid4())[:8]}"

    # 3) Run Dataproc Serverless PySpark batch to transform + join
    run_dataproc = DataprocCreateBatchOperator(
        task_id="run_dataproc_transform_join",
        gcp_conn_id="gcp_conn",
        project_id=project_id,
        region="us-central1",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": f"gs://{bucket}/scripts/transform_join_ecommerce.py",
                "args": [
                    "--project", project_id,
                    "--dataset", dataset,
                    "--temp_bucket", f"gs://{temp_bucket}"
                ],
                "jar_file_uris": []
            },
            "runtime_config": {
                "version": "2.2",
            },
            "environment_config": {
                "execution_config": {
                    "service_account": "gcp-ecomm-accnt@ecommerce-pipeline-464806.iam.gserviceaccount.com",
                    "network_uri": "projects/ecommerce-pipeline-464806/global/networks/default",
                    "subnetwork_uri": "projects/ecommerce-pipeline-464806/regions/us-central1/subnetworks/default",
                }
            },
        },
        batch_id=batch_id,
    )

    dummy_message = BashOperator(
            task_id='Dummy_Message_OP',
            bash_command='echo "Job Done !!!"',
        )

    # 4) Define task ordering
    [load_products, load_orders] >> run_dataproc >> dummy_message

dag = gcs_to_bq_dataproc_ecommerce()