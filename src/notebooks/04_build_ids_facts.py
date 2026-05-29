# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Build IDS Facts

# COMMAND ----------

dbutils.widgets.text("staging_catalog", "staging")
dbutils.widgets.text("ids_catalog", "ids")
dbutils.widgets.text("schema_name", "retail")

staging_catalog = dbutils.widgets.get("staging_catalog").lower()
ids_catalog = dbutils.widgets.get("ids_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()
staging = f"{staging_catalog}.{schema_name}"
ids = f"{ids_catalog}.{schema_name}"

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.fact_order
COMMENT 'Integrated order header fact with shipment outcomes'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'fact')
AS
SELECT
  lower(o.order_id) AS order_id,
  lower(o.customer_id) AS customer_id,
  lower(o.store_id) AS store_id,
  o.order_date,
  lower(o.order_status) AS order_status,
  s.promised_delivery_date,
  s.delivered_date,
  lower(s.shipment_status) AS shipment_status,
  coalesce(s.delay_days, 0) AS delay_days,
  CASE WHEN coalesce(s.delay_days, 0) > 0 THEN true ELSE false END AS is_late_delivery,
  current_timestamp() AS integrated_at
FROM {staging}.raw_orders o
LEFT JOIN {staging}.raw_shipments s
  ON lower(o.order_id) = lower(s.order_id)
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.fact_order_item
COMMENT 'Integrated order item fact with product margin context'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'fact')
AS
SELECT
  lower(oi.order_item_id) AS order_item_id,
  lower(oi.order_id) AS order_id,
  lower(oi.product_id) AS product_id,
  cast(oi.quantity AS int) AS quantity,
  cast(oi.unit_price AS decimal(12,2)) AS unit_price,
  cast(oi.line_amount AS decimal(12,2)) AS line_amount,
  p.category,
  p.supplier_id,
  cast(p.unit_cost AS decimal(12,2)) AS unit_cost,
  cast((oi.unit_price - p.unit_cost) * oi.quantity AS decimal(12,2)) AS margin_amount,
  current_timestamp() AS integrated_at
FROM {staging}.raw_order_items oi
LEFT JOIN {ids}.dim_product p
  ON lower(oi.product_id) = p.product_id
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.fact_shipment
COMMENT 'Integrated shipment fact'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'fact')
AS
SELECT
  lower(order_id) AS order_id,
  promised_delivery_date,
  delivered_date,
  lower(shipment_status) AS shipment_status,
  cast(delay_days AS int) AS delay_days,
  CASE WHEN delay_days > 0 THEN true ELSE false END AS is_late_delivery,
  current_timestamp() AS integrated_at
FROM {staging}.raw_shipments
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.fact_return
COMMENT 'Integrated return fact with estimated refund amount'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'fact')
AS
SELECT
  lower(r.return_id) AS return_id,
  lower(r.order_id) AS order_id,
  r.return_date,
  lower(r.return_reason) AS return_reason,
  cast(sum(oi.line_amount) AS decimal(12,2)) AS estimated_refund_amount,
  current_timestamp() AS integrated_at
FROM {staging}.raw_returns r
LEFT JOIN {ids}.fact_order_item oi
  ON lower(r.order_id) = oi.order_id
GROUP BY r.return_id, r.order_id, r.return_date, r.return_reason
""")

spark.sql(f"""
CREATE OR REPLACE TABLE {ids}.fact_supplier_event
COMMENT 'Integrated supplier event fact'
TBLPROPERTIES ('poc.layer' = 'ids', 'poc.table_type' = 'fact')
AS
SELECT
  lower(supplier_event_id) AS supplier_event_id,
  lower(supplier_id) AS supplier_id,
  event_date,
  lower(event_type) AS event_type,
  lower(affected_region) AS affected_region,
  current_timestamp() AS integrated_at
FROM {staging}.raw_supplier_events
""")

for table_name in ["fact_order", "fact_order_item", "fact_shipment", "fact_return", "fact_supplier_event"]:
    print(f"{ids}.{table_name}: {spark.table(f'{ids}.{table_name}').count()} rows")
