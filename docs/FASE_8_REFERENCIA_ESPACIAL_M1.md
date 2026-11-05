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

Portanto, **não está confirmado** que os 780 Mi1 possam ser automaticamente cruzados com `root_id` do snapshot FAFB v783 a partir dos arquivos já disponíveis no repositório público.

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
