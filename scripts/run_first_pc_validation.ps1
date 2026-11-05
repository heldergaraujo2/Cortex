$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$ExpectedBranch = "data/fafb-v783-inputs"
$CurrentBranch = (git branch --show-current).Trim()
if ($CurrentBranch -ne $ExpectedBranch) {
    throw "Branch incorreta: '$CurrentBranch'. Mude para '$ExpectedBranch' antes de executar."
}

git diff --quiet
if ($LASTEXITCODE -ne 0) { throw "Há alterações locais não commitadas. Preserve-as e revise o git status antes de testar." }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw "Há alterações staged locais. Preserve-as e revise o git status antes de testar." }

git fetch origin
if ($LASTEXITCODE -ne 0) { throw "Falha em git fetch origin." }
$LocalSha = (git rev-parse HEAD).Trim()
$RemoteSha = (git rev-parse "origin/$ExpectedBranch").Trim()
if ($LocalSha -ne $RemoteSha) {
    throw "A branch local não está sincronizada com origin/$ExpectedBranch. Execute git pull --ff-only e rode novamente."
}

$RequiredFiles = @(
    "data/raw/fafb_v783/consolidated_cell_types.csv.gz",
    "data/raw/fafb_v783/connections_princeton.csv.gz",
    "data/raw/fafb_v783/coordinates.csv.gz",
    "data/raw/fafb_v783/column_assignment.csv.gz"
)
foreach ($File in $RequiredFiles) {
    if (-not (Test-Path (Join-Path $RepoRoot $File))) {
        throw "Arquivo de dados ausente: $File. Não será iniciado nenhum teste parcial."
    }
}

$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Host "Criando ambiente virtual local .venv..."
    py -3.12 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Não foi possível criar .venv com Python 3.12." }
}

Write-Host "Instalando dependências apenas no ambiente virtual do projeto..."
& $Python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar pip." }
& $Python -m pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar Cortex e dependências de teste." }

$ReportDir = Join-Path $RepoRoot "artifacts\pc-validation"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

Write-Host ""
Write-Host "[1/6] Testes automatizados..."
& $Python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "A suíte de testes falhou. Consulte a saída acima." }

Write-Host ""
Write-Host "[2/6] Auditoria de cobertura das colunas..."
& $Python scripts\inspect_fafb_columns.py --data-dir data\raw\fafb_v783 --output (Join-Path $ReportDir "column-assignment.json")
if ($LASTEXITCODE -ne 0) { throw "Falha na auditoria de column_assignment." }

Write-Host ""
Write-Host "[3/6] Baseline estrutural ME_L..."
& $Python scripts\run_fafb_baseline.py --data-dir data\raw\fafb_v783 --neuropil ME_L --output (Join-Path $ReportDir "baseline-ME_L.json")
if ($LASTEXITCODE -ne 0) { throw "Falha na baseline ME_L." }

Write-Host ""
Write-Host "[4/6] Baseline estrutural ME_R..."
& $Python scripts\run_fafb_baseline.py --data-dir data\raw\fafb_v783 --neuropil ME_R --output (Join-Path $ReportDir "baseline-ME_R.json")
if ($LASTEXITCODE -ne 0) { throw "Falha na baseline ME_R." }

Write-Host ""
Write-Host "[5/6] Frentes espaço-temporais ME_L..."
& $Python scripts\run_fafb_spatiotemporal.py --data-dir data\raw\fafb_v783 --neuropil ME_L --output (Join-Path $ReportDir "spatiotemporal-ME_L.json")
if ($LASTEXITCODE -ne 0) { throw "Falha no diagnóstico espaço-temporal ME_L." }

Write-Host ""
Write-Host "[6/6] Frentes espaço-temporais ME_R..."
& $Python scripts\run_fafb_spatiotemporal.py --data-dir data\raw\fafb_v783 --neuropil ME_R --output (Join-Path $ReportDir "spatiotemporal-ME_R.json")
if ($LASTEXITCODE -ne 0) { throw "Falha no diagnóstico espaço-temporal ME_R." }

Write-Host ""
Write-Host "VALIDAÇÃO LOCAL CONCLUÍDA."
Write-Host "Relatórios: $ReportDir"
Write-Host "Os arquivos originais em data\raw\fafb_v783 não foram modificados."
