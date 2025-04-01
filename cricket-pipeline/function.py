from googleapiclient.discovery import build


def trigger_df_job(cloud_event,environment):   
 
    service = build('dataflow', 'v1b3')
    project = "dataflow-airflow-455502"

    template_path = "gs://dataflow-templates-us-central1/latest/GCS_Text_to_BigQuery"

    template_body = {
        "jobName": "bq-load-df",  # Provide a unique name for the job
        "parameters": {
        "javascriptTextTransformGcsPath": "gs://btmn_rank/udf.js",
        "JSONPath": "gs://btmn_rank/bq.json",
        "javascriptTextTransformFunctionName": "transform",
        "outputTable": "dataflow-airflow-455502.cricket_data.odi_rankings",
        "inputFilePattern": "gs://btmn_rank/batsmen_rankings.csv",
        "bigQueryLoadingTemporaryDirectory": "gs://btmn_rank/temp_dir",
        }
    }

    request = service.projects().templates().launch(projectId=project,gcsPath=template_path, body=template_body)
    response = request.execute()
    print(response)
