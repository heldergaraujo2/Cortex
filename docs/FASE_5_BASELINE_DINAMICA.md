# Fase 5 — baseline dinâmica estrutural mínima

## Objetivo e limite

Implementar uma primeira dinâmica determinística e reproduzível sobre o subgrafo FAFB v783 validado. Esta baseline mede apenas propagação abstrata de atividade ao longo das arestas dirigidas L1 → Mi1/Tm3 → T4. Não é um modelo biofísico, não simula retina ou movimento espacial e não testa seletividade direcional.

## Modelo v0

- Estado por neurónio: taxa abstrata rᵢ ∈ [0,1].
- Atualização síncrona: rᵢ[t+1] = (1−λ)rᵢ[t] + λ·clip(uᵢ[t], 0, 1).
- Entrada: pulso ON sintético, aplicado aos neurónios L1 do piloto.
- Propagação: soma ponderada das taxas pré-sinápticas, usando apenas um neuropilo por execução.
- Peso de engenharia: syn_count / soma(syn_count de entradas do neurónio pós), calculado dentro do neuropilo escolhido.
- Parâmetros iniciais de engenharia: λ=0,5; 20 passos; amplitude 1,0; duração 2 passos; limiar estrutural 5.
- Plasticidade desligada.
- Controlo: execução sem estímulo.
- Ablações: remover Mi1 e remover Tm3 separadamente. Os pesos são normalizados uma única vez no grafo intacto; a ablação remove os nós/arestas da via sem renormalizar as entradas restantes. A população de leitura T4 permanece fixa entre cenários, contando como zero as células que perdem todas as entradas modeladas.
- Métricas: média de taxa abstrata em toda a população T4 do piloto por passo, pico, passo do pico e curvas por subtipo T4a–T4d. O número de T4 com arestas de entrada no neuropilo é reportado separadamente.

Cada execução seleciona exatamente um neuropilo (ME_L ou ME_R). Linhas de neuropilos diferentes nunca são agregadas. syn_count é proxy estrutural normalizado, não eficácia fisiológica calibrada. Todos os sinais são não negativos; o código não infere sinal a partir de neurotransmissores.

## Experimentos reais

Executar separadamente para ME_L e ME_R:

```powershell
python scripts/run_fafb_baseline.py --neuropil ME_L --output fafb_v783_baseline_ME_L.json
python scripts/run_fafb_baseline.py --neuropil ME_R --output fafb_v783_baseline_ME_R.json
```

O workflow de validação publica ambos os relatórios como artefatos. As métricas são específicas ao neuropilo e à configuração.

## Critérios de aceitação

1. Testes sintéticos demonstram propagação em dois estágios, determinismo, controlo zero, limites [0,1], validação de parâmetros e ablações.
2. A CI executa a baseline nos dois neuropilos sem agregação.
3. Os relatórios registam manifesto/hash de origem, neurónios, arestas, readout T4 e parâmetros.
4. O pulso deve produzir atividade distinta do controlo zero quando há caminhos no neuropilo; caso contrário, registar resultado negativo sem ajustar parâmetros retroativamente.
5. Nenhuma afirmação de movimento ou seletividade direcional.

## Estado epistémico

- **CONFIRMADO:** os dados estruturais e a tabela de colunas passaram validação de ingestão e cobertura na Fase 4.
- **CONFIRMADO:** o código implementa atualização determinística abstrata e mantém neuropilos separados.
- **HIPÓTESE DE ENGENHARIA:** normalizar syn_count por alvo e aplicar atualização rate-based é uma escolha útil para testar propagação.
- **DESCONHECIDO:** se estes parâmetros ou a dinâmica representam atividade neuronal biológica.
- **DESCONHECIDO:** se o subcircuito reduzido discrimina direções visuais; este experimento não responde a isso.


## Nota metodológica da primeira execução e correção de ablações

A primeira execução real do workflow (run #41, commit anterior à correção) confirmou que o pulso propagava e o controlo sem estímulo permanecia em zero. A inspeção do artefato revelou, porém, que as ablações estavam renormalizando os pesos restantes e alterando a população T4 medida. Esses resultados de ablação não são comparáveis e ficam **supersedidos**, não devem ser usados para inferência.

Correção aplicada em `cortex/dynamics.py`: os pesos são calculados uma única vez no grafo intacto; depois a ablação remove nós/arestas sem redistribuir os pesos removidos. O conjunto T4 de leitura permanece fixo nos quatro cenários, incluindo T4 sem entradas restantes, que contribuem com taxa zero. Teste dedicado verifica que o peso de uma via restante não aumenta após a ablação e que o readout não muda.

A aceitação da Fase 5 depende da nova execução real da CI com esta correção.


## Resultado da execução real — gate v0 aprovado (2026-11-04)

Workflow FAFB v783 Data Validation #48, commit `2868cd7046fd474bcb1cf7bc33dc818454fd9aa9`: **sucesso**. Artefato: https://github.com/heldergaraujo2/Cortex/actions/runs/41943528584. O artefato contém os relatórios de validação, manifesto e os dois relatórios de baseline.

Cortex CI #86, no mesmo commit, passou em Python 3.11, 3.12 e 3.13 com **45 testes aprovados em cada versão**: https://github.com/heldergaraujo2/Cortex/actions/runs/41943528569.

| Métrica | ME_L | ME_R |
|---|---:|---:|
| Neurónios no modelo | 11.355 | 11.355 |
| Arestas elegíveis | 19.841 | 19.970 |
| População T4 de leitura fixa | 6.243 | 6.243 |
| T4 com entrada modelada no grafo intacto | 3.131 | 3.102 |
| Pico médio T4 com pulso | 0,188023 | 0,185258 |
| Passo do pico (índice começando em zero) | 4 | 4 |
| Pico sem estímulo | 0 | 0 |
| Pico após ablação Mi1 | 0,036454 | 0,035259 |
| Redução após ablação Mi1 | 80,61% | 80,97% |
| Pico após ablação Tm3 | 0,151570 | 0,149999 |
| Redução após ablação Tm3 | 19,39% | 19,03% |

A população T4 de leitura permanece fixa em todos os cenários; células sem entrada após ablação contribuem com taxa zero. Pesos são normalizados no grafo intacto e não são redistribuídos após ablação.

### Interpretação estrita

- **CONFIRMADO:** o pulso sintético global aplicado aos 1.775 neurónios L1 gera propagação determinística até a população T4 nos dois neuropilos; o controlo sem estímulo permanece em zero.
- **CONFIRMADO:** nesta configuração computacional, a remoção de Mi1 reduz o pico médio de T4 em cerca de 81%; remover Tm3 reduz cerca de 19%.
- **HIPÓTESE DE ENGENHARIA:** a assimetria observada reflete a topologia e a regra de pesos escolhidas nesta baseline.
- **DESCONHECIDO:** se a assimetria representa a contribuição biológica real de Mi1/Tm3. Não há pesos fisiológicos calibrados, sinais inibitórios, atrasos biológicos, entradas visuais espaciais nem comparação experimental.
- **NÃO DEMONSTRADO:** movimento, seletividade direcional, aprendizagem ou comportamento. O pulso é uniforme/global e não usa posições de colunas.

**Conclusão:** Fase 5 concluída apenas como baseline estrutural rate-based v0, reproduzível e testada. Não equivale a um modelo biológico validado.
