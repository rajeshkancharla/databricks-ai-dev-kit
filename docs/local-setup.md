# Local Setup

## Current Tooling Status

Installed or available locally:

- Python 3.13.0
- uv 0.11.7
- Node.js 24.14.1
- npm 11.6.0
- Databricks CLI 1.0.0, installed locally under `.tools/databricks-cli`

The `.tools` folder is intentionally ignored by Git because it contains downloaded binaries.

## Databricks CLI Wrapper

Use this wrapper from the repository root:

```powershell
.\scripts\dbx.ps1 version
```

It calls the local CLI binary at:

```text
.tools\databricks-cli\databricks.exe
```

## Authenticate To Free Edition Workspace

Get the workspace URL from your Databricks browser tab. It should look similar to:

```text
https://dbc-xxxxxxxx-xxxx.cloud.databricks.com
```

Then run:

```powershell
.\scripts\dbx.ps1 auth login --host https://your-workspace-url
```

The CLI opens a browser login flow. After login, choose a profile name such as:

```text
free-edition
```

Verify authentication:

```powershell
.\scripts\dbx.ps1 auth profiles
.\scripts\dbx.ps1 current-user me --profile free-edition
```

## Next POC Step

After authentication succeeds:

1. Install Databricks AI Dev Kit skills into this repo.
2. Create a minimal Databricks Asset Bundle.
3. Generate a small synthetic dataset.
4. Run the first workspace smoke test.

## AI Dev Kit Installed Configuration

Databricks AI Dev Kit version `0.1.12` is installed for:

- Codex: `.agents/skills`
- GitHub Copilot: `.github/skills`
- Codex MCP: `.codex/config.toml`
- VS Code Copilot MCP: `.vscode/mcp.json`

The installer was run with:

```powershell
$env:DEVKIT_CHANNEL='stable'
$env:PATH = (Resolve-Path .tools\databricks-cli).Path + ';' + $env:PATH
.\.tools\ai-dev-kit\install.ps1 --profile free-edition --tools copilot,codex --force --silent
```

For GitHub Copilot in VS Code:

- Open this repository folder in VS Code.
- Open Copilot Chat in Agent mode.
- Use the tool icon or "Configure Tools" control to enable the `databricks` MCP server if needed.

For Codex:

- Open Codex from this repository folder so it can see `.agents/skills` and `.codex/config.toml`.
