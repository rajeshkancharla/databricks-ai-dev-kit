# Databricks AI Dev Kit POC Plan

## Phase 1: Local Repository Setup

Objective: create a repeatable project that can be committed to GitHub.

Tasks:

- Create a GitHub repository.
- Add this local repository as the remote.
- Add project documentation.
- Install Databricks AI Dev Kit skills into the repo.
- Commit the baseline.

Deliverable:

- A GitHub repo containing setup notes, skill configuration, and generated POC code.

## Phase 2: Skills-Only Assistant Test

Objective: test whether Databricks skills improve GitHub Copilot and Codex output without connecting to live Databricks APIs.

Tasks:

- Ask the assistant to generate a simple Databricks Asset Bundle.
- Ask the assistant to create a small bronze, silver, and gold pipeline structure.
- Ask the assistant to create a job definition.
- Ask the assistant to produce a README explaining deployment.

Deliverable:

- A generated project skeleton that can be reviewed without incurring Databricks compute cost.

## Phase 3: Free Edition Or Trial Workspace Test

Objective: run the smallest useful Databricks workload.

Tasks:

- Create the Databricks sandbox.
- Authenticate the Databricks CLI.
- Upload a small synthetic dataset.
- Create Unity Catalog objects if supported by the sandbox.
- Run a notebook or SQL transformation.
- Capture setup commands and any limitations.

Deliverable:

- A working minimal Databricks pipeline using safe sample data.

## Phase 4: MCP Evaluation

Objective: test whether MCP tools add enough value to justify the extra setup and governance.

Tasks:

- Configure the Databricks MCP server in a dev-only context.
- Allow read-only inspection first.
- Test listing catalogs, schemas, jobs, and workspace objects.
- Run one safe query.
- Compare assistant behavior with and without MCP.

Deliverable:

- A recommendation on whether MCP should be used for the office rollout.

## Phase 5: Office Rollout Recommendation

Objective: turn the POC into a decision document.

Tasks:

- Summarize what worked.
- Summarize what failed or was limited.
- Compare GitHub Copilot, Codex, and Genie Code.
- Define security and cost guardrails.
- Recommend a rollout path.

Deliverable:

- A short adoption guide for the team.
