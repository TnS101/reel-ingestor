param(
    [string]$RepoRoot = ".",
    [switch]$Commit,
    [string]$CommitMessage = "chore: establish Reel Ingestor baseline"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
Set-Location $root

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git was not found in PATH. Install/repair Git before continuing."
}

$createdGit = $false
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Cyan
    & git init -b main 2>$null
    if ($LASTEXITCODE -ne 0) {
        & git init
        if ($LASTEXITCODE -ne 0) { throw "git init failed" }
        & git branch -M main
        if ($LASTEXITCODE -ne 0) { throw "Unable to set branch to main" }
    }
    $createdGit = $true
} else {
    Write-Host "Existing .git detected. Inspecting repository state before continuing..." -ForegroundColor Yellow

    $gitBranchInfo = @(& git status --porcelain=v2 --branch)
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to inspect existing Git repository state."
    }

    $oidLine = $gitBranchInfo | Where-Object { $_ -like "# branch.oid *" } | Select-Object -First 1
    $hasHistory = $false
    if ($oidLine -and $oidLine -notmatch "\(initial\)$") {
        $hasHistory = $true
    }

    if ($hasHistory) {
        throw "Existing Git history detected. STOP and return this evidence to the Architect instead of forcing a new baseline."
    }

    Write-Host "Existing repository has no commits yet; safe to continue baseline preview." -ForegroundColor Green
}

$branch = (& git branch --show-current).Trim()
if (-not $branch) {
    & git branch -M main
    $branch = (& git branch --show-current).Trim()
}
if ($branch -ne "main") {
    throw "Unexpected baseline branch '$branch'. Expected 'main'."
}

if (-not (Test-Path ".gitignore")) {
    throw ".gitignore is missing. Refusing baseline staging."
}

Write-Host "`nRunning bootstrap verification..." -ForegroundColor Cyan
& "$PSScriptRoot\verify_bootstrap.ps1" -RepoRoot $root
if ($LASTEXITCODE -notin @(0,5)) {
    throw "Bootstrap verification failed before staging."
}

Write-Host "`nStaging candidate baseline for inspection..." -ForegroundColor Cyan
& git add -A
if ($LASTEXITCODE -ne 0) { throw "git add failed" }

$staged = @(& git diff --cached --name-only)
if ($staged.Count -eq 0) {
    throw "No files were staged for the baseline."
}

$forbidden = @(
    '(^|/)(cookies?[^/]*\.txt)$',
    '(^|/)\.env($|\.)',
    '(^|/)(credentials|secrets)\.',
    '(^|/)results\.jsonl$',
    '(^|/)(runs|Gold Results|browser_production_pack_v1)/',
    '(^|/)source\.(mp4|mkv|webm|mov)$',
    '(^|/)\.handoffs/',
    '(^|/)\.local_verify/',
    '(^|/)\.agent/artifacts/',
    '(^|/)(venv|\.venv)/'
)

$bad = @()
foreach ($f in $staged) {
    $norm = $f -replace '\\','/'
    foreach ($pattern in $forbidden) {
        if ($norm -match $pattern) {
            $bad += $f
            break
        }
    }
}

if ($bad.Count -gt 0) {
    Write-Host "`nFORBIDDEN/SUSPICIOUS staged files:" -ForegroundColor Red
    $bad | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    & git reset
    throw "Baseline blocked. Fix .gitignore or repository boundary before retrying."
}

Write-Host "`nCandidate baseline files:" -ForegroundColor Cyan
$staged | ForEach-Object { Write-Host "  $_" }

Write-Host "`nStaged diff stat:" -ForegroundColor Cyan
& git diff --cached --stat

if (-not $Commit) {
    Write-Host "`nPREVIEW ONLY - no commit created." -ForegroundColor Yellow
    Write-Host "Review the file list above. If correct, run again with -Commit." -ForegroundColor Yellow
    & git reset
    exit 0
}

Write-Host "`nCreating baseline commit..." -ForegroundColor Cyan
& git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    throw "git commit failed. Check Git user.name/user.email configuration and retry."
}

$status = @(& git status --short)
if ($status.Count -gt 0) {
    Write-Host "`nBaseline commit exists but worktree is not clean:" -ForegroundColor Red
    $status | ForEach-Object { Write-Host $_ }
    exit 6
}

Write-Host "`nBASELINE CREATED" -ForegroundColor Green
Write-Host "Branch: $(& git branch --show-current)"
Write-Host "Commit: $(& git rev-parse HEAD)"
Write-Host "Worktree: CLEAN" -ForegroundColor Green
