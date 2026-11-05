# Fase 8 — Referência anatômica para a malha de colunas

**Estado:** investigação documental concluída; integração de dados ainda bloqueada por identificação/crosswalk e validação de proveniência.  
**Data:** 2026-11-05  
**Branch de trabalho:** `research/phase-8-anatomical-column-reference`  
**Base:** `data/fafb-v783-inputs` em `66cb821590090561c69679cd5c2c005413bde50a`

## 1. Objetivo

Substituir a hipótese de conversão global direta `XYZ → p/q` por um processo anatômico em etapas, verificável e rastreável. A meta imediata não é inferir posições para todos os neurônios: é reproduzir, em um subconjunto de referência, a relação entre arborizações M10 de Mi1, colunas da medula e a malha hexagonal publicada.

## 2. Evidência primária

Zhao et al., *Eye structure shapes neuron function in Drosophila motion vision*, Nature 646, 135–142 (2025), DOI: https://doi.org/10.1038/s41586-025-09276-5.

O artigo descreve 780 neurônios Mi1 reconstruídos no lobo óptico direito. Os autores traçaram os ramos principais em M5 e M9–M10; os centros de massa das arborizações M10 formaram uma grade identificável. Um Mi1 próximo à fronteira foi excluído das análises posteriores porque seu centro estava claramente fora da grade dos vizinhos.

A mesma publicação descreve que a grade medular foi orientada usando a região equatorial e o meridiano central. A relação entre medula e olho foi estabelecida com dados de microtomografia da cabeça e direções de visualização das facetas. A malha da retina e a da medula são invertidas esquerda-direita pelo quiasma óptico.

Fontes:
- Artigo e métodos: https://www.nature.com/articles/s41586-025-09276-5
- Texto integral: https://pmc.ncbi.nlm.nih.gov/articles/PMC12488493/
- Código dos autores: https://github.com/reiserlab/eyemap_T4

## 3. O que o código original efetivamente faz

Inspeção estática de `reiserlab/eyemap_T4`, branch `main`:

- `proc_eyemap.R` carrega `data/neu_Mi1.RData` e usa `Mi1_M10_xyz` como coordenadas dos centros de arborização M10 (linhas 43–44 e 80–100).
- A malha hexagonal da lente é construída com `reghex(...)` (linhas 155–160).
- O código carrega `data/med_ixy.RData` e faz correspondência entre os índices da malha medular e os índices das lentes (linhas 162–184).
- O objeto `eyemap` liga índices de Mi1 a índices de lentes; os dados são salvos em `data/eyemap.RData` (linhas 183–205 e 377–382).
- `Fig_2_EM.R` usa `Mi1_M10_xyz` e `med_ixy` para visualizar a grade medular e seus eixos.

**Interpretação:** a grade é baseada em centros de arborização M10 de neurônios Mi1 identificados, e não em uma regressão global aplicada ao ponto XYZ genérico de qualquer neurônio. A relação medula–olho é uma etapa adicional, sustentada por dados uCT e correspondências anatômicas.

## 4. Limite do material público inspecionado

O repositório dos autores contém objetos binários RData, incluindo `neu_Mi1.RData`, `Mi1_ind.RData`, `med_ixy.RData` e `eyemap.RData`. A inspeção textual dos scripts comprova a existência e o uso desses objetos, mas não permite confirmar, sem abrir os binários, se todos os registros incluem IDs CATMAID estáveis, IDs FlyWire, ou uma tabela de crosswalk reproduzível.

A inspeção linha a linha tornou a pista mais concreta. Em `Fig_2_EM.R` (linhas 121–124), os autores indexam `Mi1_M10_xyz` por `Mi1_neu_ind[match(anno_Mi1_DRA$skid, anno_Mi1$skid)]`. Em `proc_eyemap.R`, `Mi1_M10_xyz` é carregado de `neu_Mi1.RData` e usado como matriz de coordenadas M10 (linhas 43–44 e 80–100). Portanto, o código demonstra uma cadeia explícita de `skid` CATMAID → índice local `Mi1_neu_ind` → linha da matriz M10 para as anotações usadas nessa figura. Isso é mais forte que mera presença de uma coluna `skid`. Ainda não demonstra a cobertura dessa cadeia para todos os 780 Mi1, a unicidade/ausência de NA, a correspondência de cada linha à identidade celular esperada, nem um crosswalk para FAFB v783; essas propriedades dependem de inspecionar `neu_Mi1.RData` e os objetos de anotação, dimensões e alinhamento.

A função `fafbseg.flywire.skid_to_id` documenta um caminho possível quando um CATMAID skeleton ID é conhecido: baixa o esqueleto, transforma suas coordenadas para o espaço FlyWire e consulta os root IDs sobrepostos, retornando uma confiança baseada na frequência dos IDs encontrados. Isso é uma ferramenta candidata, não evidência de que os IDs de entrada já foram recuperados:
https://fafbseg-py.readthedocs.io/en/latest/source/generated/fafbseg.flywire.skid_to_id.html

## 5. Por que o método atual do Cortex não passa

O audit atual `scripts/audit_spatial_coordinate_mapping.py` agrega amostras de `coordinates.csv.gz` por `root_id` e resume XYZ pela mediana. Em seguida, ajusta modelos afins para predizer p e q em células que já possuem atribuição.

No workflow FAFB #149, o holdout aleatório apresentou:
- p MAE: 2.7379
- q MAE: 3.6058
- RMSE euclidiano p/q: 5.7097
- correspondência inteira exata: 1.50%
- dentro de um passo da malha: 11.81%

A acurácia de hemisfério de 100% é um resultado separado e não valida a localização p/q. O próprio relatório limita a interpretação: não faz previsões para neurônios sem atribuição e um resultado ruim leave-one-cell-type-out bloqueia extrapolação entre tipos.

Além disso, a mediana de posições associadas a um root ID não é equivalente ao centro de arborização M10. O arquivo de coordenadas contém posições de supervoxels; não deve ser tratado como morfologia esquelética completa nem como centro de uma arborização específica.

## 6. Pipeline proposto

### Gate 8A — Inventário e identidade dos Mi1 de referência
1. Obter e inspecionar os objetos RData relevantes do repositório dos autores em ambiente isolado.
2. Identificar quais tabelas/rownames/annotations contêm CATMAID skeleton IDs e quais são apenas índices locais.
3. Registrar para cada Mi1: identificador de origem, evidência da identidade celular, hemisfério, disponibilidade de coordenadas M10 e disponibilidade de crosswalk.
4. Não assumir que índice de linha R equivale a CATMAID ID ou FlyWire root ID.

**Critério de aprovação:** tabela de referência versionada, com proveniência e IDs explicitamente tipados; nenhuma correspondência por posição aproximada apresentada como identidade confirmada.

### Gate 8B — Crosswalk CATMAID → FlyWire
1. Para cada CATMAID skeleton ID confirmado, executar a correspondência documentada em dataset FlyWire compatível com FAFB v783.
2. Registrar root ID retornado, confiança, quantidade de nós considerados, versão/dataset e erros.
3. Investigar colisões, fragmentos, merges e raízes desatualizadas.
4. Definir limiar de confiança antes de observar o resultado final e manter casos abaixo do limiar como não resolvidos.

**Critério de aprovação:** cobertura e taxa de correspondência publicadas, amostras de auditoria manual e nenhuma identidade inferida apenas por proximidade XYZ.

### Gate 8C — Reproduzir a grade medular
1. Usar os centros M10 dos Mi1 confirmados para reproduzir a geometria local da grade.
2. Reproduzir a definição de vizinhança hexagonal e os eixos anatômicos documentados.
3. Comparar a grade reproduzida com `column_assignment.csv.gz`, mantendo hemisfério e identificador de coluna como chave composta.
4. Quantificar resíduos, regiões de borda, células omitidas e sensibilidade a Mi1 ausentes.

**Critério de aprovação:** correspondência reprodutível e avaliação espacial por região; não basta acurácia agregada global.

### Gate 8D — Generalização limitada e honesta
1. Primeiro testar outros Mi1 não usados no ajuste, se houver conjunto independente suficiente.
2. Depois avaliar se há evidência anatômica apropriada para cada tipo adicional (L1, Tm3, Mi4, Mi9, C3, CT1, TmY15 e T4).
3. Não transferir a coordenada do soma/mediana de um tipo para o centro de arborização M10 de outro tipo.
4. Para tipos sem marcador anatômico validado, manter p/q como desconhecido.

### Gate 8E — Olho e campo visual (etapa separada)
Apenas após a grade medular estar validada, reproduzir a relação medula–olho com dados uCT/facetas. Manter explícita a inversão do quiasma óptico e não interpretar eixos p/q diretamente como direções de movimento no mundo.

## 7. Contratos de dados recomendados

Cada correspondência deve preservar, no mínimo:
- `source_dataset`, `source_version`, `source_file_sha256`
- `source_neuron_id`, `source_id_type` (CATMAID skeleton ID, FlyWire root ID ou índice local)
- `flywire_root_id` (nullable), `crosswalk_method`, `crosswalk_confidence`
- `hemisphere`, `cell_type`
- `m10_center_xyz` (nullable, com unidade e referencial documentados)
- `column_p`, `column_q` (nullable)
- `assignment_method`, `evidence_status`, `exclusion_reason`

IDs locais, CATMAID IDs e FlyWire root IDs nunca devem compartilhar uma coluna sem tipo explícito. Dados ausentes não devem ser preenchidos por interpolação silenciosa.

## 8. Licenciamento e proveniência

O repositório `eyemap_T4` contém uma licença GPL-3.0 para o código. Isso não demonstra, por si só, que cada objeto RData, reconstrução neuronal ou dado uCT esteja sob a mesma licença. Antes de copiar dados derivados para o Cortex, verificar as declarações do artigo, os termos dos datasets e a licença específica de cada ativo. Manter o código de reprodução separado dos dados de origem até que a permissão esteja clara.

O dataset FAFB v783 usado pelo Cortex possui restrições de uso já registradas em `docs/DATA_PROVENANCE.md`; esta etapa não altera nem amplia essas permissões.

## 9. Estado e decisão

- **CONFIRMADO:** o estudo fornece um método anatômico publicado baseado em centros M10 de Mi1, grade medular, marcos anatômicos e correspondência com lentes uCT.
- **CONFIRMADO:** o código público implementa essa cadeia usando objetos derivados próprios.
- **CONFIRMADO:** o audit XYZ→p/q atual do Cortex falha como método de generalização.
- **FORTEMENTE INDICADO:** a próxima abordagem deve usar marcadores de arborização por camada e uma grade medular local, não o centro genérico do root ID.
- **DESCONHECIDO:** se os objetos públicos fornecem IDs CATMAID suficientes para crosswalk automático para o snapshot FAFB v783.
- **DESCONHECIDO:** se todos os Mi1 do artigo podem ser recuperados e ligados sem ambiguidades aos root IDs v783.
- **NÃO AUTORIZADO POR EVIDÊNCIA:** atribuir p/q aos neurônios não mapeados por extrapolação do ajuste afim atual.

**Decisão:** não substituir o algoritmo atual por outro modelo preditivo ainda. Primeiro recuperar e validar a tabela de identidade e os centros M10. O audit atual permanece como diagnóstico negativo e deve continuar impedindo extrapolações não validadas.


## 10. Validação de integração documental

- **CI Cortex #189:** sucesso no commit `e4873cd702a411ed771b8b4ee25494cd9448d85f`, com jobs aprovados em Python 3.11, 3.12 e 3.13: https://github.com/heldergaraujo2/Cortex/actions/runs/42040581437
- A execução não publicou artefatos e não executou a inspeção dos objetos RData externos. Portanto, este resultado valida apenas os testes e a integridade da branch, não os gates anatômicos 8A–8E.
- A leitura do blob público `data/neu_Mi1.RData` foi confirmada pelo GitHub (SHA `ee941396f53e813b0e12d5a1fcc64abdfec321db`), mas a API textual não retornou bytes para o objeto binário. A inspeção de conteúdo continua pendente.


## 11. Ferramenta de inventário reproduzível (Gate 8A)

Foi adicionado `scripts/inspect_mi1_reference.R`. É um utilitário de leitura que recebe os dois arquivos de origem identificados no bootstrap dos autores (`data/neu_Mi1.RData` e `data/Mi1_ind.RData`), carrega os objetos em um ambiente R isolado e exporta:
- `object_inventory.csv`: classes, tipos, comprimentos, dimensões e presença de rownames de cada objeto carregado;
- `mi1_skid_to_m10_mapping.csv`: relação por linha entre `anno_Mi1$skid`, índice local `Mi1_neu_ind` e linha/coordenadas de `Mi1_M10_xyz`, tanto para o conjunto de anotações quanto para `anno_Mi1_DRA`;
- `mapping_summary.csv` e `mapping_status.txt`: contagens de correspondências, duplicatas, índices válidos e coordenadas finitas. O script rejeita `skid` duplicado em `anno_Mi1` como ambíguo, em vez de aceitar silenciosamente o primeiro resultado de `match()`.

Execução em clone local do repositório dos autores, usando uma cópia do script do Cortex:

```powershell
Rscript D:\Cortex\scripts\inspect_mi1_reference.R `
  D:\eyemap_T4\data\neu_Mi1.RData `
  D:\eyemap_T4\data\Mi1_ind.RData `
  D:\Cortex\phase8_mi1_inventory
```

Ajustar os caminhos locais conforme necessário. O script não chama `source()`, não executa os scripts de figura, não grava nos arquivos de origem e não faz chamadas à CATMAID/FlyWire. A saída descreve apenas a cadeia de índices local do artigo; não constitui crosswalk para FAFB v783. A ferramenta foi adicionada ao branch, mas **ainda não foi executada contra os RData originais**, pois os bytes binários não puderam ser obtidos neste ambiente. Nenhum resultado quantitativo deve ser presumido antes dessa execução.


## Atualização — dados de referência importados (2026-11-05)

Os dois arquivos RData requeridos pelo Gate 8A agora estão versionados em `data/external/eyemap_T4/`:

- `neu_Mi1.RData` — upstream Git blob SHA `ee941396f53e813b0e12d5a1fcc64abdfec321db`.
- `Mi1_ind.RData` — upstream Git blob SHA `bc4933282664a84361c8318d8b4a1d54a728529a`.

A importação foi executada pelo workflow [Import eyemap_T4 reference data](https://github.com/heldergaraujo2/Cortex/actions/runs/42048560799), que baixou os arquivos do repositório original e comparou `git hash-object` com os Git blob SHA publicados pelos autores. O workflow terminou com sucesso; portanto, a identidade byte a byte dos dois arquivos está verificada.

A proveniência e a ressalva de licença estão em `data/external/eyemap_T4/README.md`. Os arquivos permanecem dados de terceiros. A licença específica dos arquivos não está separadamente indicada; preservar atribuição e restrição não comercial conservadoramente até confirmação dos autores.

**Estado do Gate 8A:** os insumos agora estão disponíveis no repositório, mas o script R ainda precisa ser executado contra eles. Nenhuma contagem de neurônios, taxa de correspondência, cobertura ou conclusão anatômica é inferida apenas da importação.


## Resultados empíricos e correção da semântica dos índices (2026-11-05)

Execuções R 4.4.1:
- [Inventário estrutural #2](https://github.com/heldergaraujo2/Cortex/actions/runs/42049602085) — sucesso; artefato estrutural inspecionado.
- [Inventário com mapeamento inverso e cross-check DRA](https://github.com/heldergaraujo2/Cortex/actions/runs/42050752606) — sucesso; R 4.4.1 executou o script corrigido e publicou o artefato.

| Objeto/medida | Resultado observado |
|---|---:|
| `Mi1` | 780 elementos |
| `anno_Mi1` | 780 linhas |
| `Mi1_M10_xyz` | 779 x 3 |
| `Mi1_neu_ind` | 779 índices inteiros únicos |
| `anno_Mi1_DRA` | 42 linhas |
| Linhas de anotação presentes em `Mi1_neu_ind` | 779/780 |
| Linha de anotação ausente | 752 |
| `skid` da linha 752 | `15578998` |
| DRA derivado por mapeamento inverso | 42/42, ordem exata |

**Correção conceitual:** a estrutura demonstra que `Mi1_neu_ind` lista, na ordem das linhas de `Mi1_M10_xyz`, os índices correspondentes em `anno_Mi1`. Portanto, para uma anotação com linha `k`, a linha M10 é `match(k, Mi1_neu_ind)`. Não se deve usar `Mi1_neu_ind[k]` como se o vetor fosse um mapa direto. A expressão inversa reproduz exatamente `Mi1_ind_DRA` (42 índices, mesma ordem), um cross-check independente fornecido no arquivo dos autores.

Assim, a interpretação anterior de duas células finais sem coordenadas estava errada: os IDs nas linhas 779 e 780 podem ser associados às linhas M10 778 e 779, respectivamente. A única anotação sem coordenada na lista é a linha 752 (`skid=15578998`). Não se imputa nem inventa coordenada para ela.

O script `scripts/inspect_mi1_reference.R` foi corrigido para inverter a relação e registrar um cross-check exato com `Mi1_ind_DRA`. A linha 123 de `Fig_2_EM.R` usa a expressão direta `Mi1_neu_ind[match(...)]`, que diverge do índice DRA de referência para as duas células finais; registrar como possível inconsistência no script de figura, não como evidência para alterar os dados.

**Estado:** estrutura e semântica do vetor fortemente indicadas; cobertura local de 779/780 pelo mapeamento inverso, com uma exclusão explícita. O script corrigido executou com sucesso e o cross-check automatizado DRA foi TRUE (42/42, correspondência exata em ordem). Gate 8A está aprovado somente para a relação local CATMAID-index-M10, não para o crosswalk FAFB v783 nem para validação biológica da grade. Ainda não existe crosswalk CATMAID→FAFB v783, nem validação biológica de toda a grade.

O artefato corrigido [phase8-mi1-inventory](https://github.com/heldergaraujo2/Cortex/actions/runs/42050752606) inclui `dra_index_crosscheck.csv`, `mapping_summary.csv`, `mi1_skid_to_m10_mapping.csv`, `mapping_status.txt`, `mi1_object_structure.txt` e `object_inventory.csv`.
