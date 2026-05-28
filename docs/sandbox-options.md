# Databricks Sandbox Options

## Option 1: Databricks Free Edition

Best for:

- Personal learning.
- Non-commercial experimentation.
- Trying Databricks concepts before asking for company access.
- Running small sample-data demos.

Pros:

- No payment required.
- Forever free within fair usage limits.
- Includes one serverless workspace.
- Good enough for a low-risk AI Dev Kit skills POC.

Important limitations:

- Intended for non-commercial use.
- Limited compute size and usage.
- Serverless compute only.
- One workspace and one metastore.
- No account console or account-level APIs.
- No SSO or SCIM.
- Some features are unavailable, including Lakebase database instances.
- Not covered by support or SLA.
- Databricks may train on data in Free Edition, so do not use proprietary office data.

Recommended use in this POC:

- Use sample or synthetic data only.
- Validate assistant behavior, skills, generated project structure, notebooks, jobs, SQL, and Databricks Asset Bundle patterns.
- Avoid testing enterprise governance, networking, SSO, private connectivity, or production controls.

## Option 2: Databricks Free Trial

Best for:

- Business or office evaluation.
- Testing with proprietary data.
- Evaluating full Databricks platform features.
- Proving that the workflow could be adopted by a team.

Pros:

- Designed for commercial evaluation.
- Includes free usage credits for a limited trial window.
- Better fit for an office POC.
- Can be upgraded to a paid account later.

Important cost notes:

- Trial credits are time-limited.
- If a payment method or marketplace subscription is connected, the account can convert to pay-as-you-go after credits or trial time are exhausted.
- Cancel or remove billing details before the trial ends if you do not want charges.
- Terminate compute resources before cancellation.

Recommended use in this POC:

- Use a work email if evaluating for the office.
- Use strict dev-only resources.
- Keep data small.
- Prefer serverless or small compute.
- Tag resources with `project=ai-dev-kit-poc`.
- Set auto-stop or auto-termination wherever available.

## Recommendation

For the first pass, use Databricks Free Edition if you only need to learn and demo the workflow with synthetic data.

For an office-facing POC, use the Databricks free trial because it is explicitly designed for business evaluation and proprietary data.

## Cost Control Checklist

- Use sample or synthetic data until the environment is approved.
- Keep data volume tiny, for example a few CSV files under 10 MB.
- Use one workspace.
- Use one SQL warehouse or serverless compute path.
- Stop apps, jobs, and warehouses after testing.
- Do not leave scheduled jobs running.
- Review usage daily during the trial.
- Avoid GPU, large model serving, large vector search, and long-running apps in the first POC.
- Keep all generated code in GitHub so the environment can be recreated and deleted.
