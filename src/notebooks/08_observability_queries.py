# Databricks notebook source
# MAGIC %md
# MAGIC # 08 - Observability Queries

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("staging_catalog", "staging")
dbutils.widgets.text("ids_catalog", "ids")
dbutils.widgets.text("cds_catalog", "cds")
dbutils.widgets.text("schema_name", "retail")

staging_catalog = dbutils.widgets.get("staging_catalog").lower()
ids_catalog = dbutils.widgets.get("ids_catalog").lower()
cds_catalog = dbutils.widgets.get("cds_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()

tables = [
    (staging_catalog, schema_name, "raw_orders", "staging"),
    (staging_catalog, schema_name, "raw_order_items", "staging"),
    (ids_catalog, schema_name, "fact_order", "ids"),
    (ids_catalog, schema_name, "fact_order_item", "ids"),
    (cds_catalog, schema_name, "daily_sales_summary", "cds"),
    (cds_catalog, schema_name, "store_fulfilment_summary", "cds"),
    (cds_catalog, schema_name, "data_quality_results", "cds"),
]

rows = []
for catalog, schema, table_name, layer in tables:
    full_name = f"{catalog}.{schema}.{table_name}"
    rows.append((layer, full_name, spark.table(full_name).count()))

summary_df = spark.createDataFrame(rows, "layer string, table_name string, row_count long").withColumn("observed_at", F.current_timestamp())
summary_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{cds_catalog}.{schema_name}.pipeline_run_summary")

display(summary_df.orderBy("layer", "table_name"))
