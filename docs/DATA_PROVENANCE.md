# Proveniência e licença dos dados FAFB v783

**Snapshot:** FlyWire FAFB v783, outubro de 2023.  
**Fonte:** FlyWire Codex, produtos estáticos FAFB v783.  
**Licença dos dados públicos FlyWire:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Esta licença é separada da licença do código Cortex.

## Produtos presentes na branch experimental

Os três ficheiros abaixo estão versionados em `data/raw/fafb_v783/` e foram verificados pelo workflow FAFB Data Validation #110:

| Ficheiro | Tamanho (bytes) | Linhas de dados | SHA-256 |
|---|---:|---:|---|
| `consolidated_cell_types.csv.gz` | 901.707 | 138.327 | `8aba246d71dc40361677493629972ce3883048c3d02010adc42bda22962a1a2d` |
| `connections_princeton.csv.gz` | 68.456.801 | 5.342.446 | `445f996bf6c4b1803b9ba186189138a3061ff8623aa94c0abcf38af30a5bd48b` |
| `coordinates.csv.gz` | 5.314.546 | 238.909 | `14337121f451f98c2576cee72c24409ada5aaf7948b7c7ca8de9040296840e05` |

O ficheiro de atribuição espacial derivado `column_assignment.csv.gz` tem 45.528 linhas e SHA-256 `bdf4ce7f62cc63493d53eefad3816ff2dfd08b190e97b35a492e0e453df2f0f6`. É um produto de trabalho do Cortex sobre IDs FAFB; não é um ficheiro bruto fornecido pelo Codex.

## Produto descarregado durante a CI

`neurons.csv.gz` é descarregado durante o workflow a partir do recurso público do Codex, sem ser versionado no repositório:

`https://storage.googleapis.com/flywire-data/codex/data/fafb/783/neurons.csv.gz`

- 139.255 registos.
- SHA-256 observado: `6a6b3759e635f0f35a677d169052362131ec61d95f55919298b55c43fce4e719`.
- Contém `nt_type`, `nt_type_score` e médias de neurotransmissores.
- Não contém `nt_type_verified`; os campos presentes são previsões e scores, não validação fisiológica curada.

## Proveniência dos resultados

- Workflow de validação real: FAFB Data Validation #110, run `41951036288`, artefato ID `13381600336`.
- Auditoria T4: 53.284 linhas de entrada candidatas, 7.028 IDs pré-sinápticos, 6.236 IDs T4.
- Auditoria das previsões: 50.630 linhas com `nt_type` não vazio, 2.654 vazias, zero divergências internas entre previsão não vazia por neurónio e o rótulo da linha de conexão. Esta é consistência interna dos produtos Codex, não validação independente.

Os relatórios completos estão em:
- `docs/FASE_7_AUDITORIA_INPUTS_T4.md`
- `docs/FASE_7_MODELO_T4_ASSINADO.md`

## Licença, atribuição e uso

A página oficial de diretrizes FlyWire declara que os dados do public release são distribuídos sob CC BY-NC 4.0 e identifica v783 como o snapshot público de outubro de 2023. O uso e a redistribuição dos dados derivados devem respeitar atribuição e restrição não comercial da licença. Não remover os avisos de proveniência nem apresentar os dados como produzidos pelo Cortex.

Citações científicas recomendadas:
1. Dorkenwald, S. et al. (2024). *Neuronal wiring diagram of an adult brain*. Nature 634, 124–138. https://doi.org/10.1038/s41586-024-07558-y
2. Schlegel, P. et al. (2024). *Whole-brain annotation and multi-connectome cell typing of Drosophila*. Nature 634, 139–152. https://doi.org/10.1038/s41586-024-07686-5
3. FlyWire public-release guidelines and Codex citation guidance: https://home.flywire.ai/guidelines

**Importante:** esta documentação não substitui aconselhamento jurídico. Se o projeto vier a ter distribuição comercial, confirmar previamente as condições aplicáveis com os responsáveis do FlyWire.
