# Repository tasks (Windows PowerShell 5.1). Usage: .\tasks.ps1 <task> [-Module <name>]
param(
    [Parameter(Position = 0)] [string] $Task = 'help',
    [string] $Module = ''
)

$root = $PSScriptRoot
Set-Location -LiteralPath $root
$py = Join-Path $root '.venv\Scripts\python.exe'
$bin = Join-Path $root '.venv\Scripts'
$modules = @('contracts', 'world', 'process', 'dataset', 'oracle', 'learner', 'activations',
             'prediction', 'topology', 'analysis', 'experiment', 'executors')
$checks = @('check_imports.py', 'check_file_sizes.py', 'check_state_files.py')

function Show-Help {
    Write-Host 'Tasks:'
    Write-Host '  .\tasks.ps1 test -Module <module>   run tests/<module> with pytest'
    Write-Host '  .\tasks.ps1 affected               pytest folders for changed and untracked files'
    Write-Host '  .\tasks.ps1 checks                 run the three repository checks'
    Write-Host '  .\tasks.ps1 reproduce-figures      run topo-pilot report'
    Write-Host '  .\tasks.ps1 lock                   write requirements.lock (pip freeze)'
    Write-Host '  .\tasks.ps1 help                   show this list'
}

if ($Task -eq 'help') {
    Show-Help
    exit 0
}
if (-not (Test-Path -LiteralPath $py)) {
    Write-Host "missing interpreter: $py"
    exit 1
}

switch ($Task) {
    'test' {
        if (-not $Module) { Write-Host 'usage: .\tasks.ps1 test -Module <module>'; exit 2 }
        if ($modules -notcontains $Module) { Write-Host "unknown module: $Module"; exit 2 }
        & $py -m pytest ("tests/" + $Module) -q
        exit $LASTEXITCODE
    }
    'affected' {
        $tracked = @(git diff --name-only HEAD 2>$null)
        $untracked = @(git ls-files --others --exclude-standard)
        $changed = @($tracked + $untracked | Where-Object { $_ })
        & $py (Join-Path $root 'tools\affected_tests.py') --changed $changed
        exit $LASTEXITCODE
    }
    'checks' {
        $failed = 0
        foreach ($script in $checks) {
            & $py (Join-Path $root ('tools\' + $script))
            if ($LASTEXITCODE -ne 0) { $failed = 1 }
        }
        exit $failed
    }
    'reproduce-figures' {
        & (Join-Path $bin 'topo-pilot.exe') report
        exit $LASTEXITCODE
    }
    'lock' {
        & $py -m pip freeze --exclude-editable | Out-File -FilePath (Join-Path $root 'requirements.lock') -Encoding ascii
        exit $LASTEXITCODE
    }
    default {
        Write-Host "unknown task: $Task"
        Show-Help
        exit 2
    }
}
