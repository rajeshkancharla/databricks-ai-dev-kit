# POC Runbook

## Prerequisites

- Databricks Free Edition workspace is available.
- Databricks CLI profile `free-edition` is authenticated.
- Unity Catalog catalogs exist and use lower-case names:
  - `staging`
  - `ids`
  - `cds`

## Validate The Bundle

```powershell
.\scripts\dbx.ps1 bundle validate --target dev
```

## Deploy The Bundle

```powershell
.\scripts\dbx.ps1 bundle deploy --target dev
```

## Run The Job

```powershell
.\scripts\dbx.ps1 bundle run retail_data_engineering_poc --target dev
```

## Expected Tables

Staging:

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

IDS:

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

CDS:

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
