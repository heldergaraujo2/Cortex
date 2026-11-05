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

## 6. Integração estrutural e auditoria das previsões concluídas

O importador separado `cortex/t4_inputs.py` preserva as 53.284 linhas candidatas, 7.028 IDs pré-sinápticos, 6.236 IDs T4 e 143 grupos por tipo/neuropilo/rótulo. O workflow FAFB #99 executou a importação sobre os dados reais e terminou com sucesso.

Também foi obtido em CI o produto público `neurons.csv.gz` do snapshot 783. O módulo `cortex/t4_annotations.py` compara as previsões por neurónio com os rótulos das linhas de conexão:
- 7.028/7.028 IDs pré-sinápticos encontrados.
- 50.630 linhas têm previsão não vazia; 2.654 linhas correspondem a neurónios sem rótulo.
- Zero divergências entre rótulos não vazios por neurónio e rótulos da conexão.
- Mi9 é o caso menos robusto: 3.700 linhas GLUT, 544 GABA, 2 ACH e 1.434 sem rótulo; score mediano 0,58.

Esta concordância é apenas consistência interna dos produtos Codex, não validação independente. O ficheiro contém `nt_type` previsto e `nt_type_score`, mas não `nt_type_verified`. Nenhuma aresta recebeu sinal fisiológico confirmado.

O workflow FAFB #110 terminou com sucesso e publicou `fafb_v783_t4_neuron_annotations.json`. A suíte Cortex CI #155 aprovou 88 testes em Python 3.11, 3.12 e 3.13 e executou o demo CLI em todas as versões. A execução FAFB #110 validou também a auditoria real de previsões por neurónio.

### Próximos passos
1. Confirmar na próxima CI a cobertura do teste de rótulo vazio e manter a suíte verde.
2. Construir perfis estruturais por T4-alvo/subtipo, separando neuropilo, tipo pré-sináptico, `nt_type`, score e `syn_count`.
3. Juntar os alvos T4 à `column_assignment` existente; investigar coordenadas e uma fonte de coluna validada para os 7.028 IDs pré-sinápticos adicionais. Não inferir p/q diretamente de coordenadas brutas.
4. Investigar uma fonte independente/curada para neurotransmissores verificados e receptores pós-sinápticos. O dump Codex v783 disponível não contém `nt_type_verified`.
5. Só então construir canais assinados derivados dos dados, mantendo desconhecidos os casos de baixa confiança ou sem evidência.
6. Executar ablações e sensibilidade ME_L/ME_R sem alterar a baseline v0; DSI biológico continua bloqueado até validar orientação e PD/ND.

