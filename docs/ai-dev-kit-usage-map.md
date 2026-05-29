# AI Dev Kit Usage Map

This file records how Databricks AI Dev Kit capabilities were used in this POC.

## Important Distinction

Databricks AI Dev Kit contributed primarily through:

- Skills and instructions installed into this repository.
- Databricks MCP configuration for Codex and GitHub Copilot.
- Databricks CLI and Asset Bundle workflows used to validate, deploy, and run the POC.

The Databricks objects were created by the generated bundle, notebooks, and Databricks CLI commands. The skills guided the structure and implementation.

## Installed AI Dev Kit Locations

| Folder | Purpose |
| --- | --- |
| `.agents/skills` | Databricks skills for Codex |
| `.github/skills` | Databricks skills for GitHub Copilot |
| `.codex/config.toml` | Codex MCP configuration |
| `.vscode/mcp.json` | VS Code / GitHub Copilot MCP configuration |
| `.ai-dev-kit` | AI Dev Kit install metadata |

## Skill To Activity Mapping

| AI Dev Kit Skill Area | Used For | Repo Files / Databricks Objects |
| --- | --- | --- |
| `databricks-bundles` | Bundle structure, variables, dev target, deploy/run workflow | `databricks.yml`, `resources/jobs.yml` |
| `databricks-jobs` | Multi-task job orchestration and task dependencies | Databricks job `retail_data_engineering_poc` |
| `databricks-unity-catalog` | Catalog/schema/table naming, managed tables, table comments, table properties | `staging.retail.*`, `ids.retail.*`, `cds.retail.*` |
| `databricks-synthetic-data-gen` | Realistic retail sample data and business incident story | `01_generate_staging_data.py`, `staging.retail.raw_*` tables |
| `databricks-dbsql` | SQL transformation patterns with `CREATE OR REPLACE TABLE AS SELECT` | ids and cds notebooks |
| `databricks-config` | Lower-case naming and environment variables through bundle parameters | `databricks.yml`, job parameters |
| `databricks-docs` | General Databricks feature guidance during setup | documentation and implementation choices |

## Commands Run

### Validate Databricks Authentication

```powershell
.\scripts\dbx.ps1 auth profiles
.\scripts\dbx.ps1 current-user me --profile free-edition
```

### Inspect Catalogs And Schemas

```powershell
.\scripts\dbx.ps1 catalogs list --profile free-edition
.\scripts\dbx.ps1 schemas list staging --profile free-edition
.\scripts\dbx.ps1 schemas list ids --profile free-edition
.\scripts\dbx.ps1 schemas list cds --profile free-edition
```

### Validate Bundle

```powershell
.\scripts\dbx.ps1 bundle validate --target dev
```

### Deploy Bundle

```powershell
.\scripts\dbx.ps1 bundle deploy --target dev
```

This uploaded local bundle files to a Databricks workspace path like:

```text
/Workspace/Users/rajesh.kancharla@outlook.com/.bundle/databricks-ai-dev-kit-data-engineering-poc/dev
```

### Run Bundle Job

```powershell
.\scripts\dbx.ps1 bundle run retail_data_engineering_poc --target dev
```

Successful run:

```text
https://dbc-a6d6b977-0a25.cloud.databricks.com/?o=7474646301195265#job/774416080885364/run/1045412354775385
```

### Verify Created Tables

```powershell
.\scripts\dbx.ps1 tables list staging retail --profile free-edition --omit-columns
.\scripts\dbx.ps1 tables list ids retail --profile free-edition --omit-columns
.\scripts\dbx.ps1 tables list cds retail --profile free-edition --omit-columns
```

## Databricks Objects Created

### Workspace Bundle Deployment

```text
/Workspace/Users/rajesh.kancharla@outlook.com/.bundle/databricks-ai-dev-kit-data-engineering-poc/dev
```

### Job

```text
[dev] retail data engineering poc
```

Bundle resource key:

```text
retail_data_engineering_poc
```

### Schemas

```text
staging.retail
ids.retail
cds.retail
```

### Staging Tables

```text
staging.retail.raw_customers
staging.retail.raw_products
staging.retail.raw_stores
staging.retail.raw_orders
staging.retail.raw_order_items
staging.retail.raw_shipments
staging.retail.raw_returns
staging.retail.raw_supplier_events
staging.retail.staging_load_summary
```

### IDS Tables

```text
ids.retail.dim_customer
ids.retail.dim_product
ids.retail.dim_store
ids.retail.fact_order
ids.retail.fact_order_item
ids.retail.fact_shipment
ids.retail.fact_return
ids.retail.fact_supplier_event
```

### CDS Tables

```text
cds.retail.daily_sales_summary
cds.retail.product_margin_summary
cds.retail.store_fulfilment_summary
cds.retail.customer_value_summary
cds.retail.late_delivery_impact
cds.retail.refund_loss_summary
cds.retail.supplier_delay_summary
cds.retail.data_quality_results
cds.retail.pipeline_run_summary
```

## Notebook Responsibility Map

| Notebook | Purpose | Main Output |
| --- | --- | --- |
| `00_setup_catalogs_and_schemas.py` | Create `retail` schemas | `staging.retail`, `ids.retail`, `cds.retail` |
| `01_generate_staging_data.py` | Generate synthetic retail source data | `staging.retail.raw_*` |
| `02_load_staging_tables.py` | Add staging metadata and load summary | `staging.retail.staging_load_summary` |
| `03_build_ids_dimensions.py` | Build cleaned dimensions | `ids.retail.dim_*` |
| `04_build_ids_facts.py` | Build integrated facts | `ids.retail.fact_*` |
| `05_build_cds_sales_metrics.py` | Build sales and customer metrics | cds sales/customer/refund summaries |
| `06_build_cds_fulfilment_metrics.py` | Build fulfilment and supplier impact metrics | cds fulfilment/late delivery summaries |
| `07_data_quality_checks.py` | Run data quality checks | `cds.retail.data_quality_results` |
| `08_observability_queries.py` | Capture row-count observability summary | `cds.retail.pipeline_run_summary` |

## Runtime Issues Found And Fixed

| Issue | Fix |
| --- | --- |
| Spark `element_at` required an `INT` index but generated expression was `BIGINT` | Cast array index expressions to `int` |
| Data quality queries with `HAVING count(*) = 0` returned no rows on pass | Rewrote checks to always return one `failed_count` row |

## Related Files

- `databricks.yml`
- `resources/jobs.yml`
- `src/notebooks/`
- `docs/poc-runbook.md`
- `docs/data-engineering-poc-design.md`
