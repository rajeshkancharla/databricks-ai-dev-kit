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
