# Superstore Data Pipeline

### 1. Data Extraction

Data is extracted from given kaggle source using kaggle api

### 2. Schema Design

Based on the dataset, we can identify several potential dimensions. For this project, we will focus on Product and Location as dimensions, and Sales as our fact table.

#### Dataset Columns and their Proposed Mapping:

Invoice ID: Fact Table (unique identifier for each transaction)

Branch: Dimension (Location)

City: Dimension (Location)

Customer Type: Fact Table (attribute of the transaction)

Gender: Fact Table (attribute of the transaction)

Product Line: Dimension (Product)

Unit Price: Fact Table (attribute of the transaction)

Quantity: Fact Table (attribute of the transaction)

Tax 5%: Fact Table (attribute of the transaction)

Total: Fact Table (measure)

Date: Fact Table (date of transaction)

Time: Fact Table (time of transaction)

Payment: Fact Table (attribute of the transaction)

COGS: Fact Table (measure)

Gross Margin Percentage: Fact Table (attribute of the transaction)

Gross Income: Fact Table (measure)

Rating: Fact Table (attribute of the transaction)

#### Dimension Tables:

DimProduct

    product_id (Primary Key, INT)

    product_line (TEXT)

DimLocation

    location_id (Primary Key, INT)

    branch (TEXT)

    city (TEXT)

Fact Table:

    FactSales

    sale_id (Primary Key, INT, from Invoice ID)

    date_id (INT)

    product_id (INT, Foreign Key to DimProduct)

    location_id (INT, Foreign Key to DimLocation)

    customer_type (TEXT)

    gender (TEXT)

    unit_price (REAL)

    quantity (INT)

    tax_5_percent (REAL)

    total (REAL)

    payment (TEXT)

    cogs (REAL)

    gross_margin_percentage (REAL)

    gross_income (REAL)

    rating (REAL)

    transaction_date (DATE)

    transaction_time (TIME)

#### Final Report

1. Calculates a cumulative sum of total sales for each branch and city combination, ordered chronologically by transaction_date and transaction_time. This helps in tracking sales performance over time within specific locations.

2. Average Rating per City: Computes the average rating across all transactions within each city, offering a quick view of customer satisfaction per location.

3. Sales Rank per Location: Ranks individual sales transactions (fs.total) within each branch and city from highest to lowest, assigning the same rank to tied sales amounts (dense ranking). This identifies the top-performing individual sales within specific branches and cities.


# Cloud Scenarios

| **Pipeline Stage**               | **Function**                                     | **GCP Service Used**             |
|----------------------------------|--------------------------------------------------|----------------------------------|
| 1. Data Extraction               | Download dataset from Kaggle                     | Cloud Function                   |
| 2. Secrets Management            | Store and access Kaggle API credentials          | Secret Manager                   |
| 3. Raw Data Storage              | Store downloaded CSV or raw files                | Cloud Storage (GCS)              |
| 4. ETL Processing                | Run Python scripts to clean/transform data       | Cloud Build or Cloud Run         |
| 5. Data Warehouse Loading        | Load transformed data into warehouse             | BigQuery                         |
| 6. Reporting Table Generation    | Create/report tables with SQL queries            | BigQuery                         |
| 7. Data Visualization            | Visualize report data with dashboards            | Looker Studio                    |


| **Pipeline Stage**               | **Function**                                                  | **GCP Service Used**                                 |
|----------------------------------|---------------------------------------------------------------|------------------------------------------------------|
| 1. DAG Triggering                | Schedule and trigger the Airflow DAG                          | **Cloud Scheduler**, **Cloud Composer (Airflow)**    |
| 2. Secrets Management            | Provide Kaggle credentials to DAG                             | **Secret Manager**                                   |
| 3. Data Extraction               | Download dataset from Kaggle                                  | **Cloud Composer (PythonOperator)**                  |
| 4. Raw Data Storage              | Store downloaded raw files (e.g. CSV)                          | **Cloud Storage** (Raw Data Bucket)                  |
| 5. File-based Trigger (Optional) | Trigger DAG when new files arrive                             | **Cloud Storage**, **Cloud Composer (Sensor)**       |
| 6. ETL Processing                | Run PySpark job to clean/transform data                       | **Cloud Dataflow**, **Cloud Composer**               |
| 7. Staging Data Storage          | Temporarily store transformed data                            | **Cloud Storage** (Staging Bucket)                   |
| 8. Data Warehouse Loading        | Load final processed data into warehouse                      | **BigQuery**                                         |
| 9. Reporting Table Generation    | Create/report tables using SQL queries                        | **BigQuery**                                         |
| 10. Data Visualization           | Build dashboards for business reporting                       | **Looker Studio**                                    |

