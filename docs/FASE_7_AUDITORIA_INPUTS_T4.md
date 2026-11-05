# Fase 7 — auditoria real dos inputs candidatos a T4

**Estado:** subetapa de inventário estrutural concluída no GitHub Actions. A modelagem assinada e a seletividade direcional continuam pendentes.

## 1. Execução reproduzível

- Dataset: FlyWire FAFB v783.
- Branch: `data/fafb-v783-inputs`.
- Workflow: FAFB v783 Data Validation #82.
- Run: https://github.com/heldergaraujo2/Cortex/actions/runs/41948702974
- Artefato: `fafb-v783-validation-report`, ID `13380560010`.
- Relatório: `fafb_v783_t4_input_audit.json`.
- SHA-256 do ZIP do artefato: `a947761f29a87e101f2b18d901a8691bc4796aa3e3cdd47dde69ad8d2fef08c7`.
- Cortex CI #122: 65 testes aprovados em Python 3.11, 3.12 e 3.13.
- A auditoria leu a tabela completa de 5.342.446 linhas de conexões. O workflow #82 terminou com sucesso e incluiu importação, validação espacial, auditoria T4, baselines e diagnósticos espaço-temporais ME_L/ME_R.

## 2. Contagens de tipos primários

Os valores abaixo são contagens de IDs com `primary_type` correspondente na tabela `consolidated_cell_types.csv.gz`, não uma medida de cobertura funcional:

| Tipo | IDs |
|---|---:|
| Mi1 | 1.581 |
| Tm3 | 1.756 |
| Mi4 | 1.532 |
| Mi9 | 1.551 |
| C3 | 1.535 |
| TmY15 | 257 |
| CT1 | 2 |
| T4a | 1.457 |
| T4b | 1.507 |
| T4c | 1.710 |
| T4d | 1.569 |

**Observação:** CT1 aparece com apenas dois IDs primários nesta tabela, embora as conexões agregadas desses neurónios produzam muitas linhas para T4. Linhas de conexão não são contagem de neurónios.

## 3. Conexões candidatas para T4

A auditoria encontrou 53.284 linhas de tabela para conexões dirigidas de Mi1, Tm3, Mi4, Mi9, C3, TmY15 ou CT1 para T4a–T4d, considerando todos os neuropilos reportados.

- Linhas ME_L: 25.904.
- Linhas ME_R: 26.656.
- Total ME_L + ME_R: 52.560.
- Soma de `syn_count` nessas linhas ME_L + ME_R: 574.359.
- Linhas em outros neuropilos: 724.
- Linhas em que um candidato pré-sináptico tinha pós-sináptico sem tipo mapeado: 59.

As somas de `syn_count` foram mantidas separadas por neuropilo e rótulo; a soma conjunta acima serve apenas como resumo das duas regiões e não representa eficácia sináptica.

### Resumo por tipo pré-sináptico nas duas regiões da medula

| Tipo | Linhas ME_L | Linhas ME_R | `syn_count` ME_L | `syn_count` ME_R |
|---|---:|---:|---:|---:|
| Mi1 | 10.472 | 10.685 | 152.302 | 155.950 |
| Tm3 | 5.254 | 5.097 | 40.489 | 39.000 |
| Mi4 | 2.175 | 2.204 | 16.223 | 16.380 |
| Mi9 | 2.783 | 2.897 | 23.099 | 23.689 |
| C3 | 519 | 726 | 2.985 | 4.316 |
| CT1 | 2.747 | 2.798 | 34.800 | 36.588 |
| TmY15 | 1.954 | 2.249 | 13.147 | 15.391 |

### Rótulos `nt_type` fornecidos no arquivo de conexões

| Rótulo | Linhas |
|---|---:|
| ACH | 31.333 |
| GABA | 17.098 |
| GLUT | 4.853 |

O resultado é misto por classe. Exemplos:
- Mi1 e Tm3 são predominantemente ACH nas linhas ME_L/ME_R, mas aparecem também algumas linhas GLUT.
- Mi4, C3, CT1 e TmY15 são predominantemente GABA nas linhas da medula; existem algumas exceções ACH em Mi4/C3/TmY15.
- Mi9 aparece com mistura de GLUT e GABA, com predomínio GLUT, e pequena quantidade ACH.

**Não converter automaticamente estes rótulos em sinal funcional.** A FAQ oficial do Codex distingue neurotransmissores previstos de campos verificados/curados e alerta que podem divergir. O relatório preserva `nt_type` literalmente. É necessário comparar esses rótulos por aresta com as anotações verificadas e com a literatura antes de atribuir sinal a uma conexão individual.

## 4. Interpretação científica permitida

**CONFIRMADO:** o snapshot FAFB v783 contém IDs primários dos sete tipos candidatos e linhas de conectividade dirigidas desses tipos para T4a–T4d, incluindo as duas regiões da medula.

**CONFIRMADO:** a distribuição de `nt_type` no arquivo não é uniforme nem perfeitamente consistente por classe. Os rótulos são reportados como fornecidos pelo produto.

**FORTEMENTE INDICADO pela literatura:** Mi1/Tm3 fornecem entradas colinérgicas predominantemente excitatórias; Mi4, C3 e CT1 são GABAérgicos e fornecem entradas inibitórias; Mi9 é glutamatérgico e atua sobre T4 via receptor GluClα, com efeito inibitório neste contexto. TmY15 é descrito como GABAérgico, mas a sua contribuição funcional específica requer cuidado.

**FORTEMENTE INDICADO pela fisiologia:** a seletividade direcional T4 envolve integração de excitação rápida e inibição espacialmente deslocada e mais lenta; isso não fornece, por si só, atrasos numéricos específicos para este snapshot.

**DESCONHECIDO:** sinal funcional de cada aresta individual do arquivo; receptores e eficácia sináptica por contato; atrasos específicos; contribuição causal de cada candidato; geometria funcional e orientação de cada arborização no modelo atual.

## 5. Decisões para a próxima subetapa

1. Manter o baseline v0 intacto como referência comparável.
2. Criar um módulo experimental separado para entradas T4 assinadas, com parâmetros explícitos e configuráveis.
3. Distinguir três conceitos: rótulo de neurotransmissor, efeito pós-sináptico e polaridade da resposta pré-sináptica ao estímulo. Em particular, não reduzir Mi9 a “GLUT = excitatório”.
4. Modelar atrasos como parâmetros de exploração/sensibilidade, não como tempos biológicos medidos.
5. Comparar estímulos preferenciais e nulos, flash estático e ausência de estímulo, com ablações por classe.
6. Só usar o termo DSI após definir corretamente a orientação local do T4 e validar a correspondência espacial relevante.

## 6. Fontes científicas

- Shinomiya et al. (2017), *The comprehensive connectome of a neural substrate for ‘ON’ motion detection in Drosophila*, eLife: https://elifesciences.org/articles/24394 — anatomia das entradas T4, fenótipos de neurotransmissores propostos e organização dendrítica; a polaridade de Mi9 é dependente do receptor.
- Gruntman et al. (2018), *Simple integration of fast excitation and offset, delayed inhibition computes directional selectivity in Drosophila*, eLife: https://elifesciences.org/articles/38167 — evidência fisiológica de integração de excitação rápida com inibição espacialmente deslocada e atrasada.
- Behnia & Desplan (2015), *Visual motion detection in Drosophila*, Annual Review of Neuroscience: https://doi.org/10.1146/annurev-neuro-080422-111929 — revisão da arquitetura e dos papéis dos canais pré-sinápticos.
- FlyWire Codex FAQ: https://codex.flywire.ai/faq — distinção entre `nt_type` previsto e `nt_type_verified` curado, estrutura dirigida das conexões e múltiplas linhas por neuropilo.

## 7. Limites

Este relatório não demonstra seletividade direcional, não calibra o modelo neuronal e não identifica o sinal funcional de cada sinapse. O próximo passo é um modelo experimental de integração assinada, comparado a controles e claramente separado dos resultados biológicos confirmados.
