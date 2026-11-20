# Importação inicial do piloto FAFB v783

## Objetivo e escopo

O importador `cortex.connectome.load_pilot_connectome` lê os produtos oficiais Codex:

- `consolidated_cell_types.csv.gz`
- `connections_princeton.csv.gz`
- `coordinates.csv.gz`

Ele cria um subgrafo estrutural reduzido para tipos primários L1, Mi1, Tm3 e variantes T4*. Não constrói dinâmica neuronal nem tenta inferir seletividade direcional.

## Executar

A partir da raiz do repositório, com Python 3.11+:

```powershell
python scripts/import_fafb_pilot.py --data-dir "D:\Cortex-data\FAFB-v783" --output "D:\Cortex-data\FAFB-v783\fafb_v783_pilot_manifest.json"
```

O comando lê os três arquivos, calcula SHA-256, valida os cabeçalhos e os campos necessários e escreve um relatório JSON. O arquivo de saída é gerado; mantenha-o fora do Git salvo se houver uma decisão explícita para publicar apenas um relatório sanitizado e pequeno.

Para executar os testes:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

## Regras de integridade

- Os arquivos de origem não são alterados.
- O importador exige as colunas esperadas e falha claramente quando faltam arquivos, IDs, coordenadas válidas ou contagens numéricas.
- IDs de neurónios são mantidos como strings para evitar perda de precisão.
- Linhas de conexão são mantidas separadas por neuropilo; não se somam linhas de diferentes neuropilos silenciosamente.
- O relatório distingue linhas da tabela de pares dirigidos únicos `(pre_root_id, post_root_id)`.
- Múltiplas linhas de coordenadas para o mesmo `root_id` são preservadas. A unidade e a interpretação física de `position` não são presumidas.
- A tabela usada é `connections_princeton`, não a versão `no_threshold`; o importador não aplica outro limiar nem afirma que a ausência de uma linha prova ausência biológica de conexão.

## Limites e licença

O output é uma extração estrutural, não um simulador. Não inclui todas as classes que podem fornecer entradas a T4 e não estabelece causalidade, pesos fisiológicos, atrasos, resposta temporal nem seletividade direcional.

Os dados públicos FAFB v783 são indicados pelo FlyWire como CC BY-NC 4.0. Preservar atribuição e respeitar a condição não comercial; ver [orientações oficiais de citação](https://join.flywire.ai/guidelines) e `data/raw/fafb_v783/README.md`.
