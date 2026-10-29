# Fontes científicas e decisão inicial de dataset

**Atualizado:** 2026-10-28  
**Estado:** seleção do dataset/circuito, aquisição dos três produtos, validação estrutural e importador inicial do subgrafo piloto concluídos e verificados por GitHub Actions. Não existe ainda simulador funcional.

## 1. Decisão para o primeiro protótipo

**Dataset selecionado: FlyWire FAFB v783 (snapshot de outubro de 2023), representando o cérebro adulto feminino completo, incluindo os lobos ópticos e sem o cordão nervoso.** Esta escolha vale para o primeiro protótipo e para circuitos iniciais dentro do cérebro; não obriga o projeto a usar FAFB em todas as fases.

Motivos:
- O âmbito corresponde diretamente à primeira meta: trabalhar com um conectoma de cérebro, sem adicionar já o cordão nervoso.
- A versão tem documentação científica extensa e é utilizada em análises e modelos publicados.
- O guia oficial FlyWire identifica explicitamente o lançamento público FAFB v783 como CC BY-NC 4.0, permitindo planear a atribuição e o uso não comercial com clareza.
- O snapshot fixo melhora a reprodutibilidade face a depender apenas de uma base de dados viva.

**Alternativa para uma fase posterior: BANC v888**, que inclui cérebro e cordão nervoso e poderá ser mais adequado a circuitos sensório-motores integrados. A licença e os produtos concretos do BANC deverão ser confirmados no depósito antes de o importar.

Esta escolha não autoriza baixar o dataset completo. O primeiro download deve limitar-se aos produtos compactos necessários para inspecionar o esquema e selecionar um circuito pequeno, depois de verificar os metadados e a licença dos arquivos concretos.

## 2. Fontes primárias/oficiais

1. **Codex — catálogo e estatísticas de datasets:** https://codex.flywire.ai/  
   O catálogo consultado lista FAFB v783 (139.255 neurónios; 3.732.460 conexões de pares neuronais no contador do Codex) e BANC v888 (158.262 neurónios; 3.037.361 conexões de pares neuronais). Esses contadores não equivalem a número de sinapses individuais e podem depender do limiar de conexão adotado.

2. **FAQ oficial do Codex:** https://codex.flywire.ai/faq  
   Confirma versões disponíveis, snapshots estáticos, diferenças entre Codex e CAVE e recomenda downloads estáticos para análise em lote. A FAQ informa limiares padrão diferentes por dataset (FAFB: 5+ sinapses por par; BANC: 3+), portanto os contadores não devem ser comparados sem harmonizar filtros.

3. **Orientações oficiais de citação/licença FlyWire:** https://flywire.ai/guidelines  
   Declara que o lançamento público FAFB v783 está sob CC BY-NC 4.0. Verificar separadamente as condições aplicáveis ao BANC e aos arquivos concretos selecionados.

4. **Dorkenwald et al. (2024), “Neuronal wiring diagram of an adult brain”, Nature:** https://www.nature.com/articles/s41586-024-07558-y  
   Referência central para o conectoma FlyWire FAFB e seus limites.

5. **Lin et al. (2024), “Network statistics of the whole-brain connectome of Drosophila”, Nature:** https://www.nature.com/articles/s41586-024-07968-y  
   Explica filtros de qualidade e limiares usados para pares conectados; um par conectado não é o mesmo que uma sinapse individual.

6. **Bates et al. (2026), “Distributed control circuits across a brain-and-cord connectome”, Nature:** https://www.nature.com/articles/s41586-026-10735-w  
   Descreve o BANC, um connectoma de cérebro e cordão nervoso. O artigo identifica o BANC como um recurso vivo e indica depósitos estáticos para reprodutibilidade.

7. **Depósito de dados BANC:** https://doi.org/10.7910/DVN/7WTH1N  
   Verificar versão, metadados, licença e checksums dos arquivos antes de baixar.

8. **FlyConnectome:** https://github.com/seung-lab/FlyConnectome  
   Ferramentas e exemplos de acesso a dados de conectoma; não substitui a validação do esquema dos arquivos que serão efetivamente usados.

## 3. Comparação preliminar

| Critério | BANC v888 | FAFB v783 |
|---|---|---|
| Âmbito | Cérebro e cordão nervoso, fêmea adulta | Cérebro adulto, incluindo lobos ópticos; sem cordão nervoso |
| Snapshot observado | 20-05-2026 | Outubro de 2023 |
| Contagem no Codex consultado | 158.262 neurónios; 3.037.361 conexões | 139.255 neurónios; 3.732.460 conexões |
| Limiar padrão no Codex | 3+ sinapses por par | 5+ sinapses por par |
| Licença | Confirmar no depósito e nos arquivos selecionados antes de uso | Guia oficial FlyWire: CC BY-NC 4.0 |
| Utilidade provável | Fase posterior para circuitos cérebro–cordão | Primeiro protótipo de cérebro e comparação com literatura |
| Estado da decisão | Alternativa futura; licença dos arquivos concretos a confirmar | **Selecionado para o primeiro protótipo** |

Os números acima são contagens do catálogo, não uma garantia de que o arquivo de conexões escolhido tenha exatamente o mesmo número de linhas. Agregação por neuropilo, autapses, limiares e versão podem mudar a contagem.

## 4. Regras antes de importar

Para cada arquivo que vier a ser utilizado, registar no manifesto:
- dataset, snapshot e data de acesso;
- nome de produto/arquivo original e URL de origem;
- versão/commit do importador;
- tamanho em bytes e SHA-256;
- licença e citação aplicáveis;
- esquema, unidades, tipos de dados e semântica das colunas;
- filtros aplicados, incluindo limiar de sinapses e agregação por neuropilo;
- se o dado é medido, anotado, previsto, inferido ou derivado.

Não guardar datasets brutos grandes no Git. Manter manifesto, scripts e fixtures sintéticas pequenas rastreadas; dados brutos, caches, bases processadas e checkpoints ficam fora do repositório.

## 5. Limites científicos confirmados

- Um connectoma é uma representação estrutural de conectividade, não uma simulação funcional pronta.
- A conectividade dirigida descreve relações pré-sinápticas e pós-sinápticas; por si só não especifica completamente dinâmica, pesos fisiológicos, atrasos, estado inicial ou regras de plasticidade.
- Tipos de neurotransmissores podem incluir previsões e anotações verificadas; esses campos não são intercambiáveis.
- Uma conexão agregada por par neuronal não é uma sinapse individual.
- Um resultado de simulação não é uma gravação da atividade de uma mosca viva.

## 6. Estado e próximos critérios

**CONFIRMADO:** fontes oficiais consultadas documentam snapshots FAFB e BANC e recomendam downloads estáticos para análise em lote.  
**CONFIRMADO:** a orientação oficial FlyWire declara CC BY-NC 4.0 para o lançamento público FAFB v783 e o Codex documenta o snapshot e os contadores apresentados acima.  
**FORTEMENTE INDICADO:** FAFB v783 é a opção mais controlável para o primeiro protótipo centrado no cérebro, dada a documentação e a licença explícita.  
**HIPÓTESE:** a escolha de FAFB v783 reduzirá a complexidade inicial de integração face a começar por um dataset que também contém o cordão nervoso.  
**DESCONHECIDO:** o circuito inicial exato, a compatibilidade dos produtos de download com o importador ainda inexistente, o custo de simulação e o esquema efetivo dos arquivos ainda não descarregados.

A seleção final do primeiro circuito só será concluída após inspecionar os metadados reais, escolher uma tarefa testável e verificar que há dados suficientes para sustentar essa tarefa.


## 7. Nota de cautela sobre licenças de depósitos relacionados

O depósito Zenodo de conectividade FAFB v783 (DOI 10.5281/zenodo.10676866) descreve o esquema dos arquivos feather e indica um arquivo de conexões proofread de aproximadamente 852 MB e um array de root IDs de aproximadamente 1,1 MB: https://zenodo.org/records/10676866. Esse depósito é um produto distinto dos CSVs estáticos sincronizados no portal Codex. Não assumir que os termos de licença, esquema ou contagens são idênticos entre os dois produtos.

As orientações públicas FlyWire para o lançamento FAFB v783 indicam CC BY-NC 4.0, enquanto depósitos derivados ou arquivos publicados separadamente podem apresentar metadados de licença próprios. Por prudência, o Cortex tratará os produtos do Codex como não comerciais e exigindo atribuição, e verificará os termos mostrados para cada arquivo exato antes de redistribuição ou uso. Em caso de conflito entre metadados do depósito e orientação do projeto, não redistribuir os dados; documentar a divergência e solicitar esclarecimento ao FlyWire.


## 8. Resultados reais da primeira inspeção dos produtos (2026-10-28)

Os arquivos enviados à branch `data/fafb-v783-inputs` foram lidos integralmente por GitHub Actions. Workflow de validação: https://github.com/heldergaraujo2/Cortex/actions/runs/40785935250 (execução da versão que preserva a agregação por neuropilo; verificar o estado final antes de aceitar resultados derivados). A primeira execução concluída com sucesso reportou:

| Produto | Registos de dados | Colunas |
|---|---:|---|
| `consolidated_cell_types.csv.gz` | 138.327 | `root_id`, `primary_type`, `additional_type(s)` |
| `connections_princeton.csv.gz` | 5.342.446 | `pre_root_id`, `post_root_id`, `neuropil`, `syn_count`, `nt_type` |
| `coordinates.csv.gz` | 238.909 | `root_id`, `position`, `supervoxel_id` |

SHA-256 calculados no GitHub Actions:
- `consolidated_cell_types.csv.gz`: `8aba246d71dc40361677493629972ce3883048c3d02010adc42bda22962a1a2d`
- `connections_princeton.csv.gz`: `445f996bf6c4b1803b9ba186189138a3061ff8623aa94c0abcf38af30a5bd48b`
- `coordinates.csv.gz`: `14337121f451f98c2576cee72c24409ada5aaf7948b7c7ca8de9040296840e05`

A primeira análise de tipo celular encontrou:
- L1: 1.775;
- Mi1: 1.581;
- Tm3: 1.756;
- T4a: 1.457; T4b: 1.507; T4c: 1.710; T4d: 1.569.

A primeira análise da tabela de conectividade encontrou registos de tabela para todos os quatro pares de tipos do piloto:
- L1 → Mi1: 1.620 linhas da tabela;
- L1 → Tm3: 6.706 linhas;
- Mi1 → T4: 21.159 linhas;
- Tm3 → T4: 10.458 linhas.

**Importante:** `connections_princeton` é uma tabela por par pré/pós e neuropilo. O número de linhas não é o número de pares neuronais únicos; um par pode aparecer em mais de um neuropilo. Não somar `syn_count` entre neuropilos sem explicitar a regra. Os valores acima são linhas observadas na tabela, não uma contagem deduplicada de arestas.

A primeira versão da análise também encontrou 11.355 IDs classificados como L1/Mi1/Tm3/T4 e correspondência de coordenadas para todos eles no arquivo `coordinates`. A versão corrigida do script preserva a agregação por neuropilo e distingue linhas da tabela de pares `(pre_root_id, post_root_id)` únicos. A execução completa da versão corrigida terminou com sucesso no workflow https://github.com/heldergaraujo2/Cortex/actions/runs/40786393103.

**Evidência:**
- **CONFIRMADO:** os três arquivos podem ser lidos como gzip/CSV; a primeira execução completa terminou com 3/3 arquivos e zero erros.
- **CONFIRMADO:** a primeira varredura identificou registos para os quatro pares de tipos de interesse.
- **FORTEMENTE INDICADO:** os produtos escolhidos são suficientes para iniciar a extração estrutural do subcircuito.
- **DESCONHECIDO:** completude funcional do circuito, correspondência de colunas visuais com T4, pesos fisiológicos, atrasos e seletividade direcional do modelo.
- **CONFIRMADO:** a execução da versão corrigida calculou os pares únicos e preservou os totais por neuropilo; o relatório JSON foi publicado como artefato do workflow.

A licença pública declarada pelo FlyWire para o lançamento FAFB v783 é CC BY-NC 4.0. A proveniência e as orientações de citação estão registadas em `data/raw/fafb_v783/README.md`; verifique novamente os termos oficiais antes de qualquer uso comercial ou redistribuição derivada.


## 9. Fecho do gate de importação estrutural do piloto (2026-10-28)

O workflow [FAFB v783 Data Validation, run 19](https://github.com/heldergaraujo2/Cortex/actions/runs/40786393103) terminou com sucesso. Executou a inspeção integral dos três CSVs comprimidos e, depois, executou o importador real sobre os mesmos arquivos. O artefato `fafb-v783-validation-report` contém `fafb_v783_validation_report.json` e `fafb_v783_pilot_manifest.json`.

- O importador carregou 11.355 IDs do conjunto L1/Mi1/Tm3/T4 e encontrou coordenadas para 11.355/11.355 IDs.
- O subgrafo importado contém 59.218 linhas de conexão entre neurónios cujos tipos primários pertencem ao conjunto piloto, preservando a separação por neuropilo.
- Os quatro pares principais têm os seguintes números de pares dirigidos únicos (deduplicados entre neuropilos): L1→Mi1 = 1.620; L1→Tm3 = 6.706; Mi1→T4 = 21.157; Tm3→T4 = 10.351.
- O manifesto regista tamanho e SHA-256 de cada arquivo de entrada.
- O workflow de testes [Cortex CI, run 61](https://github.com/heldergaraujo2/Cortex/actions/runs/40786637777) passou em Python 3.11, 3.12 e 3.13 com 23 testes, incluindo a rejeição de gzip corrompido.

**Conclusão científica limitada:** a presença de conexões estruturais para os quatro pares é confirmada nos produtos usados. Não se demonstrou que esse subgrafo reproduz movimento visual, seletividade direcional ou uma dinâmica biológica. A correspondência espacial/colunar continua pendente; `coordinates.csv.gz` não substitui a validação de `column_assignment.csv.gz`.
