# Build "READ ME FIRST - Summary of the Research So Far".
#
#   powershell -ExecutionPolicy Bypass -File docs\research_summary\build.ps1            # snapshots
#   powershell -ExecutionPolicy Bypass -File docs\research_summary\build.ps1 -Refresh   # re-read stores
#
# 1. make_figures.py writes figures/*.pdf|png (with -Refresh it first re-reads the X6S1 gate
#    statuses and the CPU ledgers into data/*.json; see make_figures.py for what it may read).
# 2. pdflatex, bibtex, pdflatex, pdflatex in a build directory outside the repository.
# 3. The PDF is copied to 00_READ_ME_FIRST_Research_Summary_So_Far/ at the repository root.
param(
    [switch]$Refresh,
    [string]$BuildDir = "X:\Downloads\topo-scratch\paper\build"
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $here "..\..")).Path
$py = Join-Path $repo ".venv\Scripts\python.exe"
$outDir = Join-Path $repo "00_READ_ME_FIRST_Research_Summary_So_Far"
$outPdf = Join-Path $outDir "READ_ME_FIRST_Research_Summary_So_Far.pdf"

$figArgs = @("-s", (Join-Path $here "make_figures.py"))
if ($Refresh) { $figArgs += "--refresh" }
& $py @figArgs
if ($LASTEXITCODE -ne 0) { throw "make_figures.py failed" }

New-Item -ItemType Directory -Force $BuildDir | Out-Null
Push-Location $here
try {
    $env:BIBINPUTS = "$here;"
    $tex = @("-interaction=nonstopmode", "-halt-on-error", "-output-directory=$BuildDir", "research_summary.tex")
    & pdflatex @tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex (pass 1) failed; see $BuildDir\research_summary.log" }
    Push-Location $BuildDir
    try { & bibtex research_summary | Out-Null } finally { Pop-Location }
    if ($LASTEXITCODE -ne 0) { throw "bibtex failed; see $BuildDir\research_summary.blg" }
    & pdflatex @tex | Out-Null
    & pdflatex @tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex (final pass) failed; see $BuildDir\research_summary.log" }
} finally { Pop-Location }

New-Item -ItemType Directory -Force $outDir | Out-Null
Copy-Item (Join-Path $BuildDir "research_summary.pdf") $outPdf -Force
Write-Output "wrote $outPdf"
