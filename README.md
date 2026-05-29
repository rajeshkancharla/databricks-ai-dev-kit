# Databricks AI Dev Kit POC

This repository is a sandbox for exploring Databricks AI Dev Kit with GitHub Copilot, Codex, and Databricks Genie Code.

## Goals

- Understand how Databricks AI Dev Kit skills work with existing coding assistants.
- Compare a skills-only workflow against a workflow with MCP tools.
- Build a small, repeatable Databricks proof of concept.
- Keep all setup notes, generated code, and decisions in GitHub for future reference.

## Recommended Sandbox

Start with Databricks Free Edition if the work is personal learning, non-commercial exploration, and uses only sample or synthetic data.

Use a Databricks free trial if the POC is for office/business evaluation, needs proprietary data, or needs fuller platform capabilities.

## Repository Structure

```text
docs/
  sandbox-options.md      Databricks account options and cost controls
  local-setup.md          Local CLI and authentication setup
  poc-plan.md             Phased POC plan
  data-engineering-poc-design.md Data engineering POC design
  poc-runbook.md          Commands to validate, deploy, and run the POC
 .agents/
  skills/                 Databricks AI Dev Kit skills for Codex
 .github/
  skills/                 Databricks AI Dev Kit skills for GitHub Copilot
 .codex/
  config.toml             Codex MCP configuration
 .vscode/
  mcp.json                VS Code Copilot MCP configuration
resources/
  jobs.yml                Databricks Job definition
scripts/
  dbx.ps1                 Wrapper for the repo-local Databricks CLI
src/
  notebooks/              Databricks notebooks for staging, ids, and cds
data/
  README.md               Placeholder for sample or synthetic data
```

## Next Steps

1. Choose the Databricks sandbox type: Free Edition or free trial.
2. Create or connect a GitHub repository remote.
3. Install the Databricks AI Dev Kit skills into this project.
4. Build the first small Databricks Asset Bundle POC.
5. Commit each experiment so the decision trail is preserved.

See `docs/local-setup.md` for Databricks CLI authentication steps.

## POC Quick Start

Validate the bundle:

```powershell
.\scripts\dbx.ps1 bundle validate --target dev
```

Deploy and run:

```powershell
.\scripts\dbx.ps1 bundle deploy --target dev
.\scripts\dbx.ps1 bundle run retail_data_engineering_poc --target dev
```
