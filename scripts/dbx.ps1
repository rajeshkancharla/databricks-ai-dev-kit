param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Arguments
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$cli = Join-Path $repoRoot ".tools\databricks-cli\databricks.exe"

if (-not (Test-Path $cli)) {
    Write-Error "Databricks CLI not found at $cli. Install it before using this wrapper."
    exit 1
}

& $cli @Arguments
exit $LASTEXITCODE
