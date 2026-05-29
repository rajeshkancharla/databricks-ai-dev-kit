# Databricks notebook source
# MAGIC %md
# MAGIC # 07 - Data Quality Checks

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
staging = f"{staging_catalog}.{schema_name}"
ids = f"{ids_catalog}.{schema_name}"
cds = f"{cds_catalog}.{schema_name}"

# COMMAND ----------

checks = [
    ("staging_raw_orders_has_rows", f"SELECT CASE WHEN count(*) = 0 THEN 1 ELSE 0 END AS failed_count FROM {staging}.raw_orders", "critical"),
    ("ids_dim_customer_unique_key", f"SELECT count(*) AS failed_count FROM (SELECT customer_id FROM {ids}.dim_customer GROUP BY customer_id HAVING count(*) > 1)", "critical"),
    ("ids_fact_order_has_customer", f"SELECT count(*) AS failed_count FROM {ids}.fact_order WHERE customer_id IS NULL", "critical"),
    ("ids_order_items_positive_amount", f"SELECT count(*) AS failed_count FROM {ids}.fact_order_item WHERE line_amount <= 0", "critical"),
    ("cds_daily_sales_has_rows", f"SELECT CASE WHEN count(*) = 0 THEN 1 ELSE 0 END AS failed_count FROM {cds}.daily_sales_summary", "critical"),
    ("cds_late_delivery_impact_has_rows", f"SELECT CASE WHEN count(*) = 0 THEN 1 ELSE 0 END AS failed_count FROM {cds}.late_delivery_impact", "warning"),
]

results = []
for check_name, sql_text, severity in checks:
    failed_count = spark.sql(sql_text).collect()[0]["failed_count"]
    results.append((check_name, severity, int(failed_count), "pass" if failed_count == 0 else "fail"))

results_df = spark.createDataFrame(results, "check_name string, severity string, failed_count long, status string").withColumn("checked_at", F.current_timestamp())
results_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{cds}.data_quality_results")

display(results_df)

critical_failures = results_df.where("severity = 'critical' AND status = 'fail'").count()
if critical_failures:
    raise ValueError(f"Data quality failed with {critical_failures} critical failure(s). See {cds}.data_quality_results")
