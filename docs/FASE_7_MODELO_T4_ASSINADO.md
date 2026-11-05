# Fase 7 — protótipo de integração assinada T4

**Estado:** protótipo sintético implementado; integração com arestas e geometria real FAFB ainda pendente. Não é uma simulação biológica calibrada nem demonstração de seletividade direcional em dados reais.

## 1. Motivação

A auditoria real do FAFB v783 confirmou conexões dos candidatos Mi1, Tm3, Mi4, Mi9, C3, TmY15 e CT1 para T4a–T4d. A literatura descreve entradas colinérgicas predominantemente excitatórias de Mi1/Tm3, entradas GABAérgicas inibitórias de Mi4/C3/CT1 e contribuição de Mi9 via glutamato/receptor GluClα, que pode atuar de forma inibitória em T4. Mi9 também apresenta respostas anticorrelacionadas a incrementos de luminância; portanto, sua contribuição não pode ser reduzida a uma regra simples `GLUT = excitação`.

O trabalho experimental de Gruntman et al. (2018) sustenta uma integração de entradas espacialmente deslocadas, com excitação rápida e inibição mais lenta, associada à supressão da direção nula. O artigo não fornece parâmetros universais que possam ser copiados diretamente para cada aresta FAFB deste snapshot.

## 2. Implementação

Arquivos:
- `cortex/t4_mechanism.py` — modelo rate-level sintético com braços de entrada assinados.
- `tests/test_t4_mechanism.py` — testes de controlo, sinal, atraso e assimetria.
- `scripts/run_t4_mechanism_demo.py` — execução reproduzível e exportação JSON.
- `.github/workflows/tests.yml` — CI executa a demonstração sintética após a suíte de testes.

Cada braço distingue explicitamente:
1. tipo(s) pré-sináptico(s);
2. rótulo de neurotransmissor;
3. sinal pós-sináptico `synaptic_sign`;
4. polaridade da resposta pré-sináptica `response_polarity`;
5. posição de campo receptivo sintética;
6. constante temporal `tau_steps`;
7. atraso `delay_steps`;
8. ganho `gain`.

Isto evita confundir neurotransmissor, polaridade da resposta do neurónio e efeito pós-sináptico.

## 3. Braços padrão do protótipo

| Braço | Tipos associados | Rótulo | Sinal sináptico | Polaridade à entrada ON | Posição | Tau | Atraso | Ganho |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Excitação rápida | Mi1, Tm3 | ACH | +1 | +1 | 0 | 1 | 0 | 1,00 |
| Inibição GABA lenta | Mi4, C3, CT1, TmY15 | GABA | -1 | +1 | +1 | 3 | 1 | 0,80 |
| Desinibição Mi9 | Mi9 | GLUT | -1 | -1 | -1 | 3 | 1 | 0,35 |

Configuração da unidade: `leak=0.7`, `maximum_rate=1.0`.

**Todos os parâmetros numéricos da tabela são escolhas de engenharia para demonstrar a lógica do modelo.** As posições -1/0/+1 não foram derivadas das coordenadas FAFB; tau e atraso não são milissegundos nem medições biológicas; ganhos não foram inferidos de `syn_count`. Os tipos associados são hipóteses informadas pela literatura, não uma atribuição de sinal por aresta.

## 4. Resultado da demonstração sintética

Estímulo: uma barra ON em posições -2, -1, 0, 1, 2; comparação com a sequência inversa. As duas sequências têm o mesmo número de eventos.

- Integral de resposta no sweep direto: 2,107407.
- Integral no sweep inverso: 1,301926.
- Índice sintético de assimetria: 0,236258.
- Sem estímulo: resposta zero.
- Braço excitatório isolado e espacialmente simétrico: assimetria zero.
- Adicionar o braço GABA reduz a integral em relação à excitação isolada para o estímulo de controlo.
- O braço Mi9, com polaridade OFF e sinapse inibitória, produz drive líquido positivo no modelo ON (desinibição).

Este índice chama-se `synthetic_directional_asymmetry_index`, não DSI. Não há mapeamento de PD/ND, campo visual, orientação de dendrito ou posições reais de neurónios. O valor 0,236258 só demonstra que esta configuração sintética pode gerar respostas diferentes para sequências invertidas.

## 5. Validação automatizada

Cortex CI #129:
- Python 3.11: 73 testes aprovados.
- Python 3.12: 73 testes aprovados.
- Python 3.13: 73 testes aprovados.

A suíte cobre:
- controlo sem estímulo;
- supressão por entrada inibitória;
- desinibição Mi9;
- sweeps opostos com energia igual;
- controlo simétrico sem assimetria;
- validação de sinais e parâmetros;
- efeito explícito do atraso.

A execução do CLI foi adicionada ao workflow CI #130; seu resultado ainda deve ser inspecionado antes de encerrar este gate.

## 6. Próximo desenvolvimento

1. Inspecionar o CI #130 e confirmar a execução do CLI.
2. Ampliar o importador de forma isolada para preservar as arestas reais dos sete candidatos, `nt_type`, neuropilo, IDs e `syn_count`, sem alterar o baseline v0.
3. Verificar separadamente as anotações previstas e verificadas do Codex; não assumir que o rótulo de cada linha é uma verdade fisiológica.
4. Investigar caminhos pré-sinápticos e correspondência espacial das classes que não possuem `column_assignment` no conjunto atual.
5. Implementar uma camada de construção de canais a partir de arestas reais, deixando sem sinal/atraso as conexões cuja evidência não seja suficiente.
6. Só depois fazer varreduras paramétricas, ablações e comparações ME_L/ME_R com dados reais.

## 7. Fontes

- Shinomiya et al. (2017), *The comprehensive connectome of a neural substrate for ‘ON’ motion detection in Drosophila*, eLife: https://elifesciences.org/articles/24394.
- Gruntman, Romani & Reiser (2018), *Simple integration of fast excitation and offset, delayed inhibition computes directional selectivity in Drosophila*, Nature Neuroscience: https://www.nature.com/articles/s41593-017-0046-4.
- FlyWire Codex FAQ: https://codex.flywire.ai/faq — diferencia `nt_type` previsto de `nt_type_verified` curado.
