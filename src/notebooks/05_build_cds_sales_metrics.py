# Databricks notebook source
# MAGIC %md
# MAGIC # 05 - Build CDS Sales Metrics

# COMMAND ----------

dbutils.widgets.text("ids_catalog", "ids")
dbutils.widgets.text("cds_catalog", "cds")
dbutils.widgets.text("schema_name", "retail")

ids_catalog = dbutils.widgets.get("ids_catalog").lower()
cds_catalog = dbutils.widgets.get("cds_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()
ids = f"{ids_catalog}.{schema_name}"
cds = f"{cds_catalog}.{schema_name}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {cds}")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {cds}.daily_sales_summary
COMMENT 'Daily sales, refund, and net sales metrics'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  o.order_date,
  s.region,
  count(DISTINCT o.order_id) AS order_count,
  count(DISTINCT o.customer_id) AS customer_count,
  cast(sum(oi.line_amount) AS decimal(14,2)) AS gross_sales_amount,
  cast(sum(coalesce(r.estimated_refund_amount, 0)) AS decimal(14,2)) AS refund_amount,
  cast(sum(oi.line_amount) - sum(coalesce(r.estimated_refund_amount, 0)) AS decimal(14,2)) AS net_sales_amount,
  cast(sum(oi.margin_amount) AS decimal(14,2)) AS gross_margin_amount,
  current_timestamp() AS calculated_at
FROM {ids}.fact_order o
JOIN {ids}.fact_order_item oi ON o.order_id = oi.order_id
JOIN {ids}.dim_store s ON o.store_id = s.store_id
LEFT JOIN {ids}.fact_return r ON o.order_id = r.order_id
GROUP BY o.order_date, s.region
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {cds}.product_margin_summary
COMMENT 'Product category sales and margin metrics'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  p.category,
  p.supplier_id,
  count(DISTINCT oi.order_id) AS order_count,
  sum(oi.quantity) AS units_sold,
  cast(sum(oi.line_amount) AS decimal(14,2)) AS gross_sales_amount,
  cast(sum(oi.margin_amount) AS decimal(14,2)) AS gross_margin_amount,
  cast(sum(coalesce(r.estimated_refund_amount, 0)) AS decimal(14,2)) AS refund_amount,
  current_timestamp() AS calculated_at
FROM {ids}.fact_order_item oi
JOIN {ids}.dim_product p ON oi.product_id = p.product_id
LEFT JOIN {ids}.fact_return r ON oi.order_id = r.order_id
GROUP BY p.category, p.supplier_id
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {cds}.customer_value_summary
COMMENT 'Customer-level sales, refund, and late delivery impact metrics'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  c.customer_id,
  c.customer_segment,
  c.region,
  count(DISTINCT o.order_id) AS order_count,
  cast(sum(oi.line_amount) AS decimal(14,2)) AS gross_sales_amount,
  cast(sum(coalesce(r.estimated_refund_amount, 0)) AS decimal(14,2)) AS refund_amount,
  sum(CASE WHEN o.is_late_delivery THEN 1 ELSE 0 END) AS late_order_count,
  current_timestamp() AS calculated_at
FROM {ids}.dim_customer c
JOIN {ids}.fact_order o ON c.customer_id = o.customer_id
JOIN {ids}.fact_order_item oi ON o.order_id = oi.order_id
LEFT JOIN {ids}.fact_return r ON o.order_id = r.order_id
GROUP BY c.customer_id, c.customer_segment, c.region
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {cds}.refund_loss_summary
COMMENT 'Refund loss metrics by return reason and region'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  r.return_reason,
  s.region,
  count(DISTINCT r.return_id) AS return_count,
  cast(sum(r.estimated_refund_amount) AS decimal(14,2)) AS estimated_refund_amount,
  current_timestamp() AS calculated_at
FROM {ids}.fact_return r
JOIN {ids}.fact_order o ON r.order_id = o.order_id
JOIN {ids}.dim_store s ON o.store_id = s.store_id
GROUP BY r.return_reason, s.region
""")

for table_name in ["daily_sales_summary", "product_margin_summary", "customer_value_summary", "refund_loss_summary"]:
    print(f"{cds}.{table_name}: {spark.table(f'{cds}.{table_name}').count()} rows")
