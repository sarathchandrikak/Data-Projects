-- 1) Create the dataset
CREATE SCHEMA IF NOT EXISTS `ecommerce-pipeline-464806.retail_data`;

-- 2) Create the products table (will be overwritten every run)
CREATE TABLE IF NOT EXISTS `ecommerce-pipeline-464806.retail_data.products` (
  product_id INT64,
  name       STRING,
  category   STRING,
  price      FLOAT64,
  in_stock      INT64
);

-- 3) Create the orders table (will be overwritten every run)
CREATE TABLE IF NOT EXISTS `ecommerce-pipeline-464806.retail_data.orders` (
  order_id   INT64,
  user_id    INT64,
  product_id INT64,
  quantity   INT64,
  order_date   TIMESTAMP
);

-- 4) Create the final enriched_orders table (append-mode)
CREATE TABLE IF NOT EXISTS `ecommerce-pipeline-464806.retail_data.enriched_orders` (
  order_id       INT64,
  user_id        INT64,
  product_id     INT64,
  name           STRING,
  category       STRING,
  price          FLOAT64,
  quantity       INT64,
  total_price    FLOAT64,
  stock          INT64,
  price_tier     STRING,   -- “Low”, “Medium”, “High”
  order_dt       DATE
);