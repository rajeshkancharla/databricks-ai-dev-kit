# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Generate Staging Data

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("staging_catalog", "staging")
dbutils.widgets.text("schema_name", "retail")

staging_catalog = dbutils.widgets.get("staging_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()
target = f"{staging_catalog}.{schema_name}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {target}")

# COMMAND ----------

customers = (
    spark.range(1, 5001)
    .withColumn("customer_id", F.format_string("cust_%05d", F.col("id")))
    .withColumn("customer_name", F.concat(F.lit("customer "), F.col("id")))
    .withColumn("region", F.element_at(F.array(F.lit("nsw"), F.lit("vic"), F.lit("qld"), F.lit("wa"), F.lit("sa")), ((F.col("id") % 5) + 1).cast("int")))
    .withColumn("customer_segment", F.when(F.col("id") % 20 == 0, "enterprise").when(F.col("id") % 5 == 0, "business").otherwise("consumer"))
    .withColumn("signup_date", F.date_add(F.to_date(F.lit("2024-01-01")), (F.col("id") % 540).cast("int")))
    .select("customer_id", "customer_name", "region", "customer_segment", "signup_date")
)

products = (
    spark.range(1, 501)
    .withColumn("product_id", F.format_string("prod_%04d", F.col("id")))
    .withColumn("product_name", F.concat(F.lit("product "), F.col("id")))
    .withColumn("category", F.element_at(F.array(F.lit("electronics"), F.lit("home"), F.lit("grocery"), F.lit("fashion"), F.lit("outdoor")), ((F.col("id") % 5) + 1).cast("int")))
    .withColumn("supplier_id", F.format_string("supp_%03d", (F.col("id") % 50) + 1))
    .withColumn("unit_cost", F.round(F.lit(5.0) + (F.col("id") % 90) * F.lit(1.7), 2))
    .withColumn("unit_price", F.round(F.col("unit_cost") * (F.lit(1.25) + (F.col("id") % 7) * F.lit(0.04)), 2))
    .select("product_id", "product_name", "category", "supplier_id", "unit_cost", "unit_price")
)

stores = (
    spark.range(1, 101)
    .withColumn("store_id", F.format_string("store_%03d", F.col("id")))
    .withColumn("store_name", F.concat(F.lit("store "), F.col("id")))
    .withColumn("region", F.element_at(F.array(F.lit("nsw"), F.lit("vic"), F.lit("qld"), F.lit("wa"), F.lit("sa")), ((F.col("id") % 5) + 1).cast("int")))
    .withColumn("fulfilment_type", F.when(F.col("id") % 4 == 0, "ship_from_store").otherwise("distribution_centre"))
    .select("store_id", "store_name", "region", "fulfilment_type")
)

orders = (
    spark.range(1, 25001)
    .withColumn("order_id", F.format_string("ord_%07d", F.col("id")))
    .withColumn("customer_id", F.format_string("cust_%05d", (F.col("id") % 5000) + 1))
    .withColumn("store_id", F.format_string("store_%03d", (F.col("id") % 100) + 1))
    .withColumn("order_date", F.date_add(F.to_date(F.lit("2026-01-01")), (F.col("id") % 120).cast("int")))
    .withColumn("order_status", F.when(F.col("id") % 97 == 0, "cancelled").otherwise("completed"))
    .select("order_id", "customer_id", "store_id", "order_date", "order_status")
)

order_items = (
    orders.select("order_id", F.expr("posexplode(array(1, 2, 3)) as (item_index, item_no)"))
    .withColumn("keep_item", ((F.abs(F.hash("order_id", "item_no")) % 100) < 70))
    .where("keep_item")
    .withColumn("order_item_id", F.concat_ws("_", F.col("order_id"), F.format_string("%02d", F.col("item_no"))))
    .withColumn("product_number", (F.abs(F.hash("order_id", "item_no")) % 500) + 1)
    .withColumn("product_id", F.format_string("prod_%04d", F.col("product_number")))
    .withColumn("quantity", ((F.abs(F.hash("order_item_id")) % 4) + 1).cast("int"))
    .join(products.select("product_id", "unit_price"), "product_id")
    .withColumn("line_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))
    .select("order_item_id", "order_id", "product_id", "quantity", "unit_price", "line_amount")
)

incident_start = F.to_date(F.lit("2026-02-15"))
incident_end = F.to_date(F.lit("2026-03-05"))

shipments = (
    orders.where("order_status = 'completed'")
    .withColumn("promised_delivery_date", F.date_add(F.col("order_date"), 4))
    .withColumn(
        "delay_days",
        F.when((F.col("order_date").between(incident_start, incident_end)) & (F.col("store_id").isin("store_002", "store_007", "store_012", "store_017")), 5)
        .when(F.col("order_id").substr(5, 7).cast("int") % 13 == 0, 2)
        .otherwise(0),
    )
    .withColumn("delivered_date", F.date_add(F.col("promised_delivery_date"), F.col("delay_days")))
    .withColumn("shipment_status", F.when(F.col("delay_days") > 0, "delivered_late").otherwise("delivered_on_time"))
    .select("order_id", "promised_delivery_date", "delivered_date", "shipment_status", "delay_days")
)

returns = (
    shipments.where((F.col("delay_days") > 0) | ((F.abs(F.hash("order_id")) % 100) < 6))
    .withColumn("return_id", F.concat(F.lit("ret_"), F.col("order_id")))
    .withColumn("return_date", F.date_add(F.col("delivered_date"), (F.abs(F.hash("order_id")) % 10 + 1).cast("int")))
    .withColumn("return_reason", F.when(F.col("delay_days") > 0, "late_delivery").otherwise("customer_preference"))
    .select("return_id", "order_id", "return_date", "return_reason")
)

supplier_events = (
    spark.range(1, 121)
    .withColumn("supplier_event_id", F.format_string("sup_evt_%04d", F.col("id")))
    .withColumn("supplier_id", F.format_string("supp_%03d", (F.col("id") % 50) + 1))
    .withColumn("event_date", F.date_add(F.to_date(F.lit("2026-01-01")), (F.col("id") % 120).cast("int")))
    .withColumn("event_type", F.when(F.col("event_date").between("2026-02-15", "2026-03-05"), "supplier_delay").otherwise("normal_variance"))
    .withColumn("affected_region", F.when(F.col("event_type") == "supplier_delay", "vic").otherwise("all"))
    .select("supplier_event_id", "supplier_id", "event_date", "event_type", "affected_region")
)

tables = {
    "raw_customers": customers,
    "raw_products": products,
    "raw_stores": stores,
    "raw_orders": orders,
    "raw_order_items": order_items,
    "raw_shipments": shipments,
    "raw_returns": returns,
    "raw_supplier_events": supplier_events,
}

for name, df in tables.items():
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{target}.{name}")
    spark.sql(f"COMMENT ON TABLE {target}.{name} IS 'Synthetic staging table for the retail data engineering POC'")
    print(f"Wrote {target}.{name}: {df.count()} rows")
