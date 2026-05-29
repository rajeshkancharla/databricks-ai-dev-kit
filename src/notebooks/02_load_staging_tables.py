# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Load Staging Tables

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("staging_catalog", "staging")
dbutils.widgets.text("schema_name", "retail")

staging_catalog = dbutils.widgets.get("staging_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()
target = f"{staging_catalog}.{schema_name}"

raw_tables = [
    "raw_customers",
    "raw_products",
    "raw_stores",
    "raw_orders",
    "raw_order_items",
    "raw_shipments",
    "raw_returns",
    "raw_supplier_events",
]

counts = []
for table_name in raw_tables:
    full_name = f"{target}.{table_name}"
    row_count = spark.table(full_name).count()
    counts.append((full_name, row_count))
    spark.sql(f"ALTER TABLE {full_name} SET TBLPROPERTIES ('poc.layer' = 'staging', 'poc.domain' = 'retail')")

summary_df = spark.createDataFrame(counts, "table_name string, row_count long").withColumn("checked_at", F.current_timestamp())
summary_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{target}.staging_load_summary")

display(summary_df)
