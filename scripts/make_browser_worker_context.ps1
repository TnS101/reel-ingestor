param(
    [Parameter(Mandatory=$true)][string]$PlanId,
    [Parameter(Mandatory=$true)][string[]]$IncludePaths,
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
Set-Location $root

if (-not (Test-Path ".git")) { throw "Git repository not initialized. Complete P001 first." }
$status = @(& git status --short)
if ($status.Count -gt 0) {
    throw "Worktree is dirty. Refusing to create Worker context from an ambiguous baseline.`n$($status -join "`n")"
}

$mandatory = @(
    "BROWSER_WORKER_RULES.md",
    "plan.md",
    "ARCHITECTURE.md",
    "PROJECT_STATE.md",
    "docs/TEST_STRATEGY.md"
)
foreach ($f in $mandatory) {
    if (-not (Test-Path $f)) { throw "Missing Worker-context file: $f" }
}

$handoffRoot = Join-Path $root ".handoffs"
$staging = Join-Path $handoffRoot ("{0}_worker_context" -f $PlanId)
$zip = Join-Path $handoffRoot ("{0}_worker_context.zip" -f $PlanId)
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging -Force | Out-Null

function Copy-RelativePath([string]$rel) {
    if ([System.IO.Path]::IsPathRooted($rel)) { throw "IncludePaths must be repo-relative: $rel" }
    $src = Join-Path $root $rel
    if (-not (Test-Path $src)) { throw "Include path not found: $rel" }
    $full = (Resolve-Path $src).Path
    if (-not $full.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Include path escapes repository root: $rel"
    }
    $dest = Join-Path $staging $rel
    if ((Get-Item $src).PSIsContainer) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
        Copy-Item (Join-Path $src "*") -Destination $dest -Recurse -Force
    } else {
        New-Item -ItemType Directory -Path (Split-Path -Parent $dest) -Force | Out-Null
        Copy-Item $src $dest -Force
    }
}

foreach ($f in $mandatory) { Copy-RelativePath $f }
foreach ($p in $IncludePaths) {
    if ($mandatory -notcontains $p) { Copy-RelativePath $p }
}

$baseline = @()
$baseline += "PLAN_ID: $PlanId"
$baseline += "ROOT: $(& git rev-parse --show-toplevel)"
$baseline += "BRANCH: $(& git branch --show-current)"
$baseline += "HEAD: $(& git rev-parse HEAD)"
$baseline += "STATUS: CLEAN"
$baseline += "TRACKED_SOURCE_CONTEXT:"
$baseline += $IncludePaths
$baseline | Set-Content (Join-Path $staging "GIT_BASELINE.txt") -Encoding UTF8

if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path (Join-Path $staging "*") -DestinationPath $zip -CompressionLevel Optimal
Remove-Item $staging -Recurse -Force

Write-Host "Created: $zip" -ForegroundColor Green
Write-Host "Baseline: $(& git rev-parse HEAD)" -ForegroundColor Cyan
