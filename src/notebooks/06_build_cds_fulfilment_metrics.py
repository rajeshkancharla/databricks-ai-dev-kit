# Databricks notebook source
# MAGIC %md
# MAGIC # 06 - Build CDS Fulfilment Metrics

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
CREATE OR REPLACE TABLE {cds}.store_fulfilment_summary
COMMENT 'Store fulfilment performance metrics'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  st.store_id,
  st.store_name,
  st.region,
  st.fulfilment_type,
  count(DISTINCT o.order_id) AS shipped_order_count,
  sum(CASE WHEN o.is_late_delivery THEN 1 ELSE 0 END) AS late_order_count,
  cast(sum(CASE WHEN o.is_late_delivery THEN 1 ELSE 0 END) / count(DISTINCT o.order_id) AS decimal(10,4)) AS late_delivery_rate,
  cast(avg(o.delay_days) AS decimal(10,2)) AS avg_delay_days,
  current_timestamp() AS calculated_at
FROM {ids}.fact_order o
JOIN {ids}.dim_store st ON o.store_id = st.store_id
WHERE o.order_status = 'completed'
GROUP BY st.store_id, st.store_name, st.region, st.fulfilment_type
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {cds}.late_delivery_impact
COMMENT 'Revenue and refund impact of late deliveries by region and category'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  st.region,
  p.category,
  count(DISTINCT o.order_id) AS affected_order_count,
  cast(sum(oi.line_amount) AS decimal(14,2)) AS affected_sales_amount,
  cast(sum(coalesce(r.estimated_refund_amount, 0)) AS decimal(14,2)) AS refund_amount,
  cast(avg(o.delay_days) AS decimal(10,2)) AS avg_delay_days,
  current_timestamp() AS calculated_at
FROM {ids}.fact_order o
JOIN {ids}.fact_order_item oi ON o.order_id = oi.order_id
JOIN {ids}.dim_product p ON oi.product_id = p.product_id
JOIN {ids}.dim_store st ON o.store_id = st.store_id
LEFT JOIN {ids}.fact_return r ON o.order_id = r.order_id
WHERE o.is_late_delivery
GROUP BY st.region, p.category
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {cds}.supplier_delay_summary
COMMENT 'Supplier delay events joined to product and sales impact'
TBLPROPERTIES ('poc.layer' = 'cds', 'poc.table_type' = 'calculated')
AS
SELECT
  se.supplier_id,
  p.category,
  se.affected_region,
  count(DISTINCT se.supplier_event_id) AS supplier_event_count,
  count(DISTINCT oi.order_id) AS impacted_order_count,
  cast(sum(oi.line_amount) AS decimal(14,2)) AS impacted_sales_amount,
  current_timestamp() AS calculated_at
FROM {ids}.fact_supplier_event se
LEFT JOIN {ids}.dim_product p ON se.supplier_id = p.supplier_id
LEFT JOIN {ids}.fact_order_item oi ON p.product_id = oi.product_id
LEFT JOIN {ids}.fact_order o ON oi.order_id = o.order_id
WHERE se.event_type = 'supplier_delay'
  AND o.order_date BETWEEN se.event_date AND date_add(se.event_date, 7)
GROUP BY se.supplier_id, p.category, se.affected_region
""")

for table_name in ["store_fulfilment_summary", "late_delivery_impact", "supplier_delay_summary"]:
    print(f"{cds}.{table_name}: {spark.table(f'{cds}.{table_name}').count()} rows")
