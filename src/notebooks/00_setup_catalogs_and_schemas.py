# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Setup Catalogs And Schemas

# COMMAND ----------

dbutils.widgets.text("staging_catalog", "staging")
dbutils.widgets.text("ids_catalog", "ids")
dbutils.widgets.text("cds_catalog", "cds")
dbutils.widgets.text("schema_name", "retail")

staging_catalog = dbutils.widgets.get("staging_catalog").lower()
ids_catalog = dbutils.widgets.get("ids_catalog").lower()
cds_catalog = dbutils.widgets.get("cds_catalog").lower()
schema_name = dbutils.widgets.get("schema_name").lower()

for identifier in [staging_catalog, ids_catalog, cds_catalog, schema_name]:
    if not identifier.replace("_", "").isalnum():
        raise ValueError(f"Only lower-case alphanumeric and underscore identifiers are supported: {identifier}")
    if identifier != identifier.lower():
        raise ValueError(f"Identifier must be lower case: {identifier}")

# COMMAND ----------

schema_comments = {
    staging_catalog: "Raw and staged retail source data for the data engineering POC",
    ids_catalog: "Integrated retail dimensions and facts for the data engineering POC",
    cds_catalog: "Calculated retail data products and metrics for the data engineering POC",
}

for catalog, comment in schema_comments.items():
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema_name} COMMENT '{comment}'")

spark.sql(f"USE CATALOG {staging_catalog}")
spark.sql(f"USE SCHEMA {schema_name}")

print(f"Prepared schemas: {staging_catalog}.{schema_name}, {ids_catalog}.{schema_name}, {cds_catalog}.{schema_name}")
