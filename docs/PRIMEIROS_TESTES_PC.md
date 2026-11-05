# Primeiros testes locais — Windows

**Objetivo:** verificar o clone Windows, a instalação Python, os testes unitários e a reprodução local dos relatórios FAFB v783 já validados no GitHub Actions.

## Pré-condições

- Clone local do repositório Cortex.
- Git e Python Launcher (`py`) instalados.
- A branch de trabalho é `data/fafb-v783-inputs`.
- Os quatro arquivos FAFB v783 estão versionados em `data/raw/fafb_v783/`.

## 1. Sincronização segura

No PowerShell, ajuste o caminho se o clone não estiver em `D:\Cortex-GitHub-Upload`:

```powershell
Set-Location "D:\Cortex-GitHub-Upload"

$dirty = git status --porcelain
if ($dirty) {
    $dirty
    throw "Há arquivos locais modificados ou não rastreados. Não troque de branch nem faça pull; revise o estado primeiro."
}

git fetch origin
if ($LASTEXITCODE -ne 0) { throw "git fetch falhou." }

git show-ref --verify --quiet refs/heads/data/fafb-v783-inputs
if ($LASTEXITCODE -eq 0) {
    git switch data/fafb-v783-inputs
} else {
    git switch --track -c data/fafb-v783-inputs origin/data/fafb-v783-inputs
}
if ($LASTEXITCODE -ne 0) { throw "Não foi possível selecionar a branch de trabalho." }

git pull --ff-only origin data/fafb-v783-inputs
if ($LASTEXITCODE -ne 0) { throw "Pull fast-forward falhou; preserve o estado e peça revisão." }

git status --short --branch
```

Não use `reset`, `clean`, `stash` ou force-push. Se o estado inicial não estiver limpo, pare e compartilhe a saída de `git status --short --branch` antes de continuar.

## 2. Executar a validação local

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_first_pc_validation.ps1
```

O script:
1. Confere a branch, ausência de alterações staged/não staged e sincronização exata com origin.
2. Confere os quatro arquivos de dados.
3. Cria `.venv` se necessário, usando Python 3.11, 3.12 ou 3.13.
4. Instala pytest e o pacote apenas no ambiente virtual local.
5. Executa os testes unitários.
6. Reproduz a auditoria de colunas, baseline estrutural e diagnóstico espaço-temporal para ME_L e ME_R.

## 3. Saídas esperadas

Os JSON são gravados em `artifacts/pc-validation/`, pasta ignorada pelo Git:
- `column-assignment.json`
- `baseline-ME_L.json`
- `baseline-ME_R.json`
- `spatiotemporal-ME_L.json`
- `spatiotemporal-ME_R.json`

O script não altera os arquivos brutos em `data/raw/fafb_v783/` e não executa operações destrutivas.

## 4. Retorno para análise

Depois da execução, compartilhe:
- a saída completa do PowerShell;
- `git status --short --branch`;
- se houver falha, o primeiro traceback completo.

Compare os JSON locais com o artefato FAFB Data Validation #71 antes de qualquer alteração no modelo. Não avance para expansão do circuito ou otimização de GPU antes deste gate.
