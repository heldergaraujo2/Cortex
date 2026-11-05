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
