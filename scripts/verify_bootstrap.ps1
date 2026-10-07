param(
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
Set-Location $root

$required = @(
    "README.md",
    "ARCHITECT_RULES.md",
    "BROWSER_WORKER_RULES.md",
    "PROJECT_STATE.md",
    "PROJECT_TRACKER.xlsx",
    "ARCHITECTURE.md",
    "plan.md",
    "docs/CURRENT_ROADMAP.md",
    "docs/DECISIONS.md",
    "docs/TEST_STRATEGY.md",
    "docs/RESEARCH_POLICY.md",
    "docs/TRACKER_POLICY.md",
    "contracts/knowledge_schema_v1.json",
    "contracts/BROWSER_SOL_PRODUCTION_PROMPT_v1_1.txt",
    "contracts/FROZEN_CONTRACTS.json",
    ".agent/templates/IMPLEMENTATION_REPORT_TEMPLATE.md",
    ".agent/templates/LOCAL_VERIFY_TEMPLATE.md"
)

Write-Host "=== REEL INGESTOR BOOTSTRAP PREFLIGHT ===" -ForegroundColor Cyan
Write-Host "Root: $root"

$missing = @()
foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        $missing += $path
        Write-Host "MISSING  $path" -ForegroundColor Red
    } else {
        Write-Host "OK       $path" -ForegroundColor Green
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`nRESULT: BLOCKED_MISSING_BOOTSTRAP_FILES" -ForegroundColor Red
    exit 2
}

Write-Host "`n=== FROZEN CONTRACT HASHES ===" -ForegroundColor Cyan
$contractMeta = Get-Content "contracts/FROZEN_CONTRACTS.json" -Raw | ConvertFrom-Json
$hashFail = $false
foreach ($c in $contractMeta.contracts) {
    if (-not (Test-Path $c.path)) {
        Write-Host "MISSING  $($c.path)" -ForegroundColor Red
        $hashFail = $true
        continue
    }
    $actual = (Get-FileHash -Algorithm SHA256 $c.path).Hash.ToLowerInvariant()
    if ($actual -ne $c.sha256.ToLowerInvariant()) {
        Write-Host "HASH FAIL $($c.path)" -ForegroundColor Red
        Write-Host "  expected: $($c.sha256)"
        Write-Host "  actual:   $actual"
        $hashFail = $true
    } else {
        Write-Host "HASH OK   $($c.path)" -ForegroundColor Green
    }
}
if ($hashFail) {
    Write-Host "`nRESULT: BLOCKED_FROZEN_CONTRACT_DRIFT" -ForegroundColor Red
    exit 3
}

Write-Host "`n=== POWERSHELL SCRIPT SYNTAX ===" -ForegroundColor Cyan
$parseFail = $false
$psScripts = Get-ChildItem -Path "scripts" -Filter "*.ps1" -File
foreach ($script in $psScripts) {
    $tokens = $null
    $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile(
        $script.FullName,
        [ref]$tokens,
        [ref]$errors
    ) | Out-Null

    if ($errors.Count -gt 0) {
        Write-Host "PARSE FAIL $($script.FullName)" -ForegroundColor Red
        foreach ($err in $errors) {
            Write-Host "  $($err.Message)" -ForegroundColor Red
        }
        $parseFail = $true
    } else {
        Write-Host "PARSE OK   scripts/$($script.Name)" -ForegroundColor Green
    }
}
if ($parseFail) {
    Write-Host "`nRESULT: BLOCKED_POWERSHELL_PARSE_ERROR" -ForegroundColor Red
    exit 7
}

Write-Host "`n=== GIT ===" -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    Write-Host "Git repository not initialized yet." -ForegroundColor Yellow
    Write-Host "RESULT: READY_FOR_GIT_BOOTSTRAP" -ForegroundColor Green
    exit 0
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "RESULT: BLOCKED_GIT_NOT_FOUND" -ForegroundColor Red
    exit 4
}

git rev-parse --show-toplevel
$gitBranchInfo = @(& git status --porcelain=v2 --branch)
$branchLine = $gitBranchInfo | Where-Object { $_ -like "# branch.head *" } | Select-Object -First 1
$oidLine = $gitBranchInfo | Where-Object { $_ -like "# branch.oid *" } | Select-Object -First 1

$branch = if ($branchLine) { ($branchLine -replace "^# branch\.head\s+", "").Trim() } else { "(unknown)" }
$head = if ($oidLine -and $oidLine -match "\(initial\)$") {
    "(unborn - no commits yet)"
} elseif ($oidLine) {
    ($oidLine -replace "^# branch\.oid\s+", "").Trim()
} else {
    "(unknown)"
}

$status = git status --short
Write-Host "Branch: $branch"
Write-Host "HEAD:   $head"
if ($status) {
    Write-Host "`nWorktree is DIRTY:" -ForegroundColor Yellow
    $status | ForEach-Object { Write-Host $_ }
    Write-Host "RESULT: BOOTSTRAP_PRESENT_GIT_DIRTY" -ForegroundColor Yellow
    exit 5
}

Write-Host "Worktree: CLEAN" -ForegroundColor Green
Write-Host "RESULT: READY_FOR_WORK" -ForegroundColor Green
