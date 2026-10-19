# Requires Python 3. Set API_URL to target an explicitly started API.
$ErrorActionPreference = 'Stop'
& python (Join-Path $PSScriptRoot '../smoke_api.py')
exit $LASTEXITCODE
