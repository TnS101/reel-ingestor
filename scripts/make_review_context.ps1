param(
    [Parameter(Mandatory=$true)][string]$PlanId,
    [Parameter(Mandatory=$true)][string]$ImplementationReport,
    [Parameter(Mandatory=$true)][string]$LocalVerify,
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
Set-Location $root

if (-not (Test-Path ".git")) { throw "Git repository not initialized." }
if (-not (Test-Path $ImplementationReport)) { throw "ImplementationReport not found: $ImplementationReport" }
if (-not (Test-Path $LocalVerify)) { throw "LocalVerify not found: $LocalVerify" }

$handoffRoot = Join-Path $root ".handoffs"
$staging = Join-Path $handoffRoot ("{0}_review_context" -f $PlanId)
$zip = Join-Path $handoffRoot ("{0}_review_context.zip" -f $PlanId)
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging -Force | Out-Null

$core = @("plan.md", "PROJECT_STATE.md", "ARCHITECTURE.md")
foreach ($f in $core) {
    Copy-Item $f (Join-Path $staging (Split-Path $f -Leaf))
}
Copy-Item $ImplementationReport (Join-Path $staging "IMPLEMENTATION_REPORT.md")
Copy-Item $LocalVerify (Join-Path $staging "LOCAL_VERIFY.md")

@(& git status --short) | Set-Content (Join-Path $staging "GIT_STATUS.txt") -Encoding UTF8
@(& git diff --stat) | Set-Content (Join-Path $staging "GIT_DIFF_STAT.txt") -Encoding UTF8
@(& git diff --name-status) | Set-Content (Join-Path $staging "GIT_DIFF_NAMES.txt") -Encoding UTF8
@(& git diff --binary) | Set-Content (Join-Path $staging "GIT_DIFF.patch") -Encoding UTF8
@(
    "BRANCH: $(& git branch --show-current)",
    "HEAD: $(& git rev-parse HEAD)"
) | Set-Content (Join-Path $staging "GIT_BASELINE_CURRENT.txt") -Encoding UTF8

if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $zip -CompressionLevel Optimal
Remove-Item $staging -Recurse -Force

Write-Host "Created: $zip" -ForegroundColor Green
