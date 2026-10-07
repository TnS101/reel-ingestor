param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Url
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = "C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe"

if (-not (Test-Path $Python)) {
    $Python = (Get-Command python -ErrorAction Stop).Source
}

& $Python "$Root\reel_ingestor.py" --url $Url --config "$Root\config.json"
exit $LASTEXITCODE
