# IRCTC PubSub-Dataflow-BigQuery

# Problem Statement

  A company needs to build a scalable, real-time data pipeline to capture change events from a transactional database, process and transform the data, 
  and store it in a data warehouse for analytics. The pipeline should also support reading additional reference files from cloud storage to enrich the 
  data before final storage.
  
# Architecture 

  Included following architecture to achieve this problem statement
    
  1. Capturing CDC events from a source database using Pub/Sub for reliable ingestion.
  2. Processing and transforming the data using Apache Beam/Dataflow to clean, enrich, and format the data.
  3. Writing the transformed data to BigQuery for further analysis and reporting.
  4. Reading UDF functions from Cloud Storage to apply transformations on the data.

  ![Image](https://github.com/sarathchandrikak/Data-Projects/blob/main/irctc-dataflow/irctc_architecture.png) 
