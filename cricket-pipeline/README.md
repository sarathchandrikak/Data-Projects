# ♦️ Real Time Automated Data Pipeline 


Sensor data is continuously uploaded to cloud storage. We must process and analyze this data in real-time, storing results in a database and visualizing key trends. This enables immediate responses to changing conditions. How can we design this? 

# ♦️ Business Use Case

A large-scale, distributed network of data sources continuously generates real-time cricket statistics and rankings. These data sources include live match feeds, player performance metrics, team records, and historical trends. The data is aggregated and uploaded to a cloud storage system, ensuring seamless access and analysis.

In this context, I am specifically working with ODI rankings from RapidAPI, which provides up-to-date rankings based on recent match performances, team points, and player statistics. By leveraging this real-time data, I aim to analyze team and player trends, predict future rankings, and derive insights into performance fluctuations. This data-driven approach can be useful for broadcasters, analysts, fantasy cricket enthusiasts, and sports strategists to make informed decisions.

# ♦️ Stages of Pipeline

1. Data Ingestion (Raw Data Storage)

    * Use Cloud composer/Apache Airflow to schedule and orchestrate the data ingestion process. (hourly/daily)
    * Store the raw JSON or CSV data from the APIs in separate GCS buckets.
3. Event Triggering/ Real time triggering (Data Arrival Notification)
   
    * Configure a Cloud Function to be triggered whenever a new file is uploaded to the GCS bucket(s) containing the raw data.
    * The Cloud Function should initiate a Dataflow job to process the uploaded data based on Eventarc trigger
      
4. Data Storage (Processed Data and Alerts)
   
   * The data transormed in dataflow gets written into big query table according to schema
     
5. Data Visualization (Real-Time Dashboard)

   * Connect looker studio to BigQuery dataset and create a Looker Studio dashboard to visualize the real-time data.


# ♦️ Architecture Diagram

![Image](https://github.com/sarathchandrikak/Data-Projects/blob/main/cricket-pipeline/pipeline.png)
