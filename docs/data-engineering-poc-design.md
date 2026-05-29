# Data Engineering POC Design

## Objective

Build a Databricks AI Dev Kit proof of concept for a typical data engineering team.

The POC focuses on medallion-style data engineering, not ML or data science. It demonstrates source ingestion, cleansing, integration, enrichment, calculated data products, orchestration, Unity Catalog governance, and repeatable deployment through Databricks Asset Bundles.

## Layer Naming

Use lower case for all Unity Catalog catalogs, schemas, and tables.

| Medallion Concept | POC Name | Unity Catalog Catalog |
| --- | --- | --- |
| Bronze | staging | `staging` |
| Silver | ids | `ids` |
| Gold | cds | `cds` |

The POC uses `staging`, `ids`, and `cds` consistently in code, SQL, bundle variables, schemas, and table names.

## Unity Catalog Namespace

Target three-level namespace:

```text
staging.retail.raw_customers
staging.retail.raw_products
staging.retail.raw_stores
staging.retail.raw_orders
staging.retail.raw_order_items
staging.retail.raw_shipments
staging.retail.raw_returns
staging.retail.raw_supplier_events

ids.retail.dim_customer
ids.retail.dim_product
ids.retail.dim_store
ids.retail.fact_order
ids.retail.fact_order_item
ids.retail.fact_shipment
ids.retail.fact_return
ids.retail.fact_supplier_event

cds.retail.daily_sales_summary
cds.retail.product_margin_summary
cds.retail.store_fulfilment_summary
cds.retail.customer_value_summary
cds.retail.late_delivery_impact
cds.retail.refund_loss_summary
```

The `retail` schema keeps the POC domain isolated inside each catalog.

## Business Story

A supplier delay and regional fulfilment issue causes late deliveries, refunds, and revenue leakage.

The data engineering workflow should answer:

- Which stores and regions had the highest late delivery rate?
- Which supplier events created measurable operational impact?
- Which products lost margin because of refunds?
- Which customers were affected by repeated delivery failures?
- What was the daily revenue, refund, and net-sales impact?
- What operational metrics should be monitored going forward?

## Synthetic Source Data

Generate coherent retail data with referential integrity:

| Table | Purpose | Approx Rows |
| --- | --- | ---: |
| `raw_customers` | Customer master data with region, segment, signup date | 5,000 |
| `raw_products` | Product master data with category, supplier, cost, price | 500 |
| `raw_stores` | Store/location data with region and fulfilment type | 100 |
| `raw_orders` | Order headers with order date, customer, store, status | 25,000 |
| `raw_order_items` | Order line items with product, quantity, price | About 50,000 |
| `raw_shipments` | Shipment status, promised date, delivered date | About 24,700 |
| `raw_returns` | Return/refund events with reason codes | About 3,000 |
| `raw_supplier_events` | Supplier delay events by supplier/category/date | 120 |

Data should include skew and anomalies:

- 80/20 revenue concentration by customers and products.
- One supplier delay incident affecting a category and region.
- Elevated late deliveries during the incident window.
- Increased refunds after late delivery.
- A few duplicate and malformed records for data quality checks.

## Notebook Plan

```text
src/notebooks/00_setup_catalogs_and_schemas.py
src/notebooks/01_generate_staging_data.py
src/notebooks/02_load_staging_tables.py
src/notebooks/03_build_ids_dimensions.py
src/notebooks/04_build_ids_facts.py
src/notebooks/05_build_cds_sales_metrics.py
src/notebooks/06_build_cds_fulfilment_metrics.py
src/notebooks/07_data_quality_checks.py
src/notebooks/08_observability_queries.py
```

## Job Orchestration

Use a Databricks Job defined through Databricks Asset Bundles.

Planned DAG:

```text
setup_catalogs_and_schemas
  -> generate_staging_data
  -> load_staging_tables
  -> build_ids_dimensions
  -> build_ids_facts
  -> build_cds_sales_metrics
  -> build_cds_fulfilment_metrics
  -> data_quality_checks
  -> observability_queries
```

Where possible, dimension and fact tasks can be split into parallel tasks after staging tables exist.

## Databricks Features Covered

- Databricks AI Dev Kit skills for data engineering.
- Databricks Asset Bundles.
- Unity Catalog catalogs, schemas, managed tables, and comments.
- Serverless SQL warehouse for DDL and validation.
- Databricks Jobs / Lakeflow Jobs with task dependencies.
- Notebook tasks with parameters.
- Synthetic data generation.
- Staging to ids to cds transformations.
- Basic data quality checks.
- Optional system table queries for job/query observability.

## AI Dev Kit Skills Used

Primary skills:

- `databricks-bundles`
- `databricks-jobs`
- `databricks-unity-catalog`
- `databricks-synthetic-data-gen`
- `databricks-dbsql`
- `databricks-config`

Optional follow-up skills:

- `databricks-spark-declarative-pipelines`
- `databricks-aibi-dashboards`

Out of scope:

- MLflow model evaluation.
- Model serving.
- Vector search.
- Agent Bricks.
- Databricks Apps.

## Workspace Setup DDL

Preferred catalog names:

```sql
CREATE CATALOG IF NOT EXISTS staging COMMENT 'Bronze layer catalog for raw and staged POC data';
CREATE CATALOG IF NOT EXISTS ids COMMENT 'Silver layer catalog for integrated data store POC data';
CREATE CATALOG IF NOT EXISTS cds COMMENT 'Gold layer catalog for calculated data store POC data';

CREATE SCHEMA IF NOT EXISTS staging.retail COMMENT 'Raw and staged retail source data';
CREATE SCHEMA IF NOT EXISTS ids.retail COMMENT 'Integrated retail dimensions and facts';
CREATE SCHEMA IF NOT EXISTS cds.retail COMMENT 'Calculated retail data products and metrics';
```

If Free Edition does not allow catalog creation through the CLI/API, create the catalogs in the Databricks UI first, then rerun schema/table setup through the bundle.

## Implementation Phases

1. Create or confirm Unity Catalog catalogs: `staging`, `ids`, `cds`.
2. Scaffold Databricks Asset Bundle files.
3. Create notebooks.
4. Generate small but realistic synthetic data.
5. Load staging tables.
6. Build ids dimensions and facts.
7. Build cds calculated summaries.
8. Add data quality checks.
9. Define Databricks Job resources.
10. Validate, deploy, and run the bundle.
11. Commit each milestone to GitHub.

## Bundle Structure

```text
databricks.yml
resources/
  jobs.yml
src/
  notebooks/
docs/
  poc-runbook.md
```
