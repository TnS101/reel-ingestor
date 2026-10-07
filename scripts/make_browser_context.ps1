param(
    [Parameter(Mandatory=$true)][string]$PlanId,
    [string]$RepoRoot = ".",
    [string]$LatestReport = "",
    [string]$LatestLocalVerify = ""
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
Set-Location $root

$files = @(
    "ARCHITECT_RULES.md",
    "PROJECT_STATE.md",
    "ARCHITECTURE.md",
    "plan.md",
    "docs/CURRENT_ROADMAP.md",
    "docs/TRACKER_POLICY.md",
    "PROJECT_TRACKER.xlsx"
)

foreach ($f in $files) {
    if (-not (Test-Path $f)) { throw "Missing architect-context file: $f" }
}

$handoffRoot = Join-Path $root ".handoffs"
$staging = Join-Path $handoffRoot ("{0}_architect_context" -f $PlanId)
$zip = Join-Path $handoffRoot ("{0}_architect_context.zip" -f $PlanId)

if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging -Force | Out-Null

foreach ($f in $files) {
    $dest = Join-Path $staging $f
    New-Item -ItemType Directory -Path (Split-Path -Parent $dest) -Force | Out-Null
    Copy-Item $f $dest
}

if (Test-Path ".git") {
    $gitState = @()
    $gitState += "ROOT: $(& git rev-parse --show-toplevel)"
    $gitState += "BRANCH: $(& git branch --show-current)"
    $gitState += "HEAD: $(& git rev-parse HEAD)"
    $gitState += "STATUS:"
    $gitState += @(& git status --short)
    $gitState | Set-Content (Join-Path $staging "GIT_STATE.txt") -Encoding UTF8
}

if ($LatestReport) {
    if (-not (Test-Path $LatestReport)) { throw "LatestReport not found: $LatestReport" }
    Copy-Item $LatestReport (Join-Path $staging "LATEST_IMPLEMENTATION_REPORT.md")
}

if ($LatestLocalVerify) {
    if (-not (Test-Path $LatestLocalVerify)) { throw "LatestLocalVerify not found: $LatestLocalVerify" }
    Copy-Item $LatestLocalVerify (Join-Path $staging "LATEST_LOCAL_VERIFY.md")
}

if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $zip -CompressionLevel Optimal
Remove-Item $staging -Recurse -Force

Write-Host "Created: $zip" -ForegroundColor Green
