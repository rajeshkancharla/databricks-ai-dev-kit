# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Build IDS Dimensions

# COMMAND ----------

dbutils.widgets.text("staging_catalog", "staging")
dbutils.widgets.text("ids_catalog", "ids")
dbutils.widgets.text("schema_name", "retail")

staging_catalog = dbutils.widgets.get("staging_catalog").lower()
ids_catalog = dbutils.widgets.get("ids_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()
staging = f"{staging_catalog}.{schema_name}"
ids = f"{ids_catalog}.{schema_name}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {ids}")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.dim_customer
COMMENT 'Integrated customer dimension'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'dimension')
AS
SELECT DISTINCT
  lower(trim(customer_id)) AS customer_id,
  initcap(trim(customer_name)) AS customer_name,
  lower(trim(region)) AS region,
  lower(trim(customer_segment)) AS customer_segment,
  signup_date,
  current_timestamp() AS integrated_at
FROM {staging}.raw_customers
WHERE customer_id IS NOT NULL
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.dim_product
COMMENT 'Integrated product dimension with price and margin attributes'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'dimension')
AS
SELECT DISTINCT
  lower(trim(product_id)) AS product_id,
  initcap(trim(product_name)) AS product_name,
  lower(trim(category)) AS category,
  lower(trim(supplier_id)) AS supplier_id,
  cast(unit_cost AS decimal(12,2)) AS unit_cost,
  cast(unit_price AS decimal(12,2)) AS unit_price,
  cast(unit_price - unit_cost AS decimal(12,2)) AS unit_margin,
  current_timestamp() AS integrated_at
FROM {staging}.raw_products
WHERE product_id IS NOT NULL
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.dim_store
COMMENT 'Integrated store dimension'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'dimension')
AS
SELECT DISTINCT
  lower(trim(store_id)) AS store_id,
  initcap(trim(store_name)) AS store_name,
  lower(trim(region)) AS region,
  lower(trim(fulfilment_type)) AS fulfilment_type,
  current_timestamp() AS integrated_at
FROM {staging}.raw_stores
WHERE store_id IS NOT NULL
""")

for table_name in ["dim_customer", "dim_product", "dim_store"]:
    print(f"{ids}.{table_name}: {spark.table(f'{ids}.{table_name}').count()} rows")
