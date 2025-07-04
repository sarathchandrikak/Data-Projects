import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    round as spark_round,
    to_date
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project",
        required=True,
        help="GCP project ID"
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="BigQuery dataset name (e.g., retail_data)"
    )
    parser.add_argument(
        "--temp_bucket",
        required=True,
        help="GCS bucket for temporary BigQuery exports (gs://â€¦)"
    )
    args = parser.parse_args()

    project = args.project
    dataset = args.dataset
    temp_bucket = args.temp_bucket

    # SparkSession with BigQuery connector
    spark = (
        SparkSession.builder
        .appName("transform_join_ecommerce")
        .getOrCreate()
    )

    # Define fully qualified table names
    products_table = f"{project}.{dataset}.products"
    orders_table   = f"{project}.{dataset}.orders"
    output_table   = f"{project}.{dataset}.enriched_orders"

    # Temporary GCS path for BigQuery connector
    bigquery_temp_dir = f"{temp_bucket}/bq_temp"

    # 1) Read products table
    products_df = (
        spark.read.format("bigquery")
        .option("table", products_table)
        .option("parentProject", project)
        .option("temporaryGcsBucket", bigquery_temp_dir)
        .load()
    )

    # 2) Transform products: add price_tier based on price
    products_transformed = products_df.withColumn(
        "price_tier",
        when(col("price") < 25.0, "Low")
        .when((col("price") >= 25.0) & (col("price") < 75.0), "Medium")
        .otherwise("High")
    ).select(
        col("product_id"),
        col("name"),
        col("category"),
        col("price"),
        col("in_stock"),
        col("price_tier")
    )

    # 3) Read orders table
    orders_df = (
        spark.read.format("bigquery")
        .option("table", orders_table)
        .option("parentProject", project)
        .option("temporaryGcsBucket", bigquery_temp_dir)
        .load()
    )

    # 4) Transform orders: add total_price = price later after join, but extract order_dt
    orders_transformed = orders_df.select(
        col("order_id"),
        col("user_id"),
        col("product_id"),
        col("quantity"),
        to_date(col("order_date")).alias("order_date")
    )

    # 5) Join products â†” orders on product_id
    joined_df = orders_transformed.join(
        products_transformed,
        orders_transformed.product_id == products_transformed.product_id,
        how="inner"
    ).select(
        orders_transformed.order_id.alias("order_id"),
        orders_transformed.user_id.alias("user_id"),
        orders_transformed.product_id.alias("product_id"),
        products_transformed.name.alias("name"),
        products_transformed.category.alias("category"),
        products_transformed.price.alias("price"),
        orders_transformed.quantity.alias("quantity"),
        spark_round(products_transformed.price * orders_transformed.quantity, 2).alias("total_price"),
        products_transformed.in_stock.alias("stock"),
        products_transformed.price_tier.alias("price_tier"),
        orders_transformed.order_date.alias("order_dt")
    )

    # 6) Write to BigQuery in append mode
    (
        joined_df.write.format("bigquery")
        .option("table", output_table)
        .option("parentProject", project)
        .option("temporaryGcsBucket", bigquery_temp_dir)
        .mode("append")
        .save()
    )

    spark.stop()
