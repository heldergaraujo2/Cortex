# Cortex — Painel de acompanhamento

> Atualizado em 2026-11-14. Este painel registra evidências verificadas, não afirma validação biológica nem representa monitoramento em tempo real.

## Estado resumido

| Área | Situação | Evidência / pendência |
| --- | --- | --- |
| Dados FAFB v783 para o piloto T4 | Confirmado na execução | Arquivos de anotações, colunas e conexões foram carregados na execução abaixo |
| Experimento T4 com grafo real | **Aprovado tecnicamente** | 66.131 arestas retidas; T4a/T4b/T4c/T4d analisados |
| Testes direcionados | **12/12 aprovados** | 7 de resposta direcional, 2 de diagnóstico e 3 de gates |
| Estabilidade numérica | **Aprovada nos gates executados** | Respostas e séries finitas, baseline próximo de zero |
| Equilíbrio dos estímulos | **Parcial** | 12 frames por direção, mas 464 eventos no eixo p e 501 no eixo q; total de eventos não igual |
| Seletividade biológica T4 | **Não validada** | Sem calibração dos eixos anatômicos e sem comparação independente com fisiologia |
| Quatro instâncias especializadas, coordenação e memória coletiva | **Planejado; integração não comprovada neste painel** | Exige implementação e testes ponta a ponta |

## Última validação examinada (não necessariamente a execução mais recente)

- **Workflow:** FAFB T4 automatic validation
- **Execução:** [#43122252091](https://github.com/heldergaraujo2/Cortex/actions/runs/43122252091)
- **Job:** [#130865353635](https://github.com/heldergaraujo2/Cortex/actions/runs/43122252091/job/130865353635)
- **Resultado:** success; commit `d59eccea137eca2bf5f88f40e05d2a0308651dc4`; branch `experiment/synthetic-neural-learning-smoke`.
- **Relatórios:** [artifact #13901431644](https://github.com/heldergaraujo2/Cortex/actions/runs/43122252091/artifacts/13901431644) (quatro JSONs: resposta, diagnóstico, gates, resumo DSI).
- **DSI descritivo:** T4a 0.0154503; T4b 0.0703704; T4c 0.1466492; T4d 0.0061020.
- **Preferências simuladas:** T4a q_negative; T4b q_positive; T4c p_positive; T4d q_negative.
- **Ressalva:** passar na CI significa que os critérios programados passaram, **não** que o modelo reproduz a fisiologia real.

## Links úteis

- [Todas as Actions](https://github.com/heldergaraujo2/Cortex/actions)
- [Workflow de validação T4](https://github.com/heldergaraujo2/Cortex/actions/workflows/fafb-t4-auto-validation.yml)
- [Roadmap](ROADMAP.md)
- [Continuidade](CONTINUIDADE.md)
- [Arquitetura](ARCHITECTURE.md)

## Próximos marcos

1. Equilibrar a intensidade/quantidade dos estímulos entre eixos p e q, com testes que falhem quando houver desigualdade; registrar controles.
2. Calibrar os eixos espaciais à anatomia T4 e confrontar respostas com dados biológicos independentes.
3. Estabelecer critérios quantitativos, controles negativos, ablações e reprodutibilidade.
4. Integrar as quatro instâncias previstas, coordenação e memória compartilhada, com testes funcionais e de aprendizagem.
5. Medir custo, desempenho, robustez e documentar limites científicos.

## Atualização automática — instalada, aguardando primeira execução verificada

O workflow [Update Cortex T4 dashboard](../.github/workflows/update-cortex-t4-dashboard.yml) foi adicionado à `main`. Quando o workflow **FAFB T4 automatic validation** terminar, o atualizador tentará ler o resultado e os JSONs publicados, registrando uma seção automática abaixo. Também pode ser iniciado manualmente pelo GitHub Actions com o número de uma execução concluída. A automação ainda precisa ser validada em uma execução real; caso o token do repositório não permita escrita, o job mostrará o erro sem modificar o painel. A seção histórica acima permanece preservada.

## Política de manutenção

Registrar sempre data, branch, commit, execução, artefatos, resultado dos gates e limitações. Não promover experimentos à `main` sem revisão dos testes e das diferenças entre branches.

<!-- T4-AUTO-START -->
## Atualização automática — validação FAFB T4

- **Execução:** [#43645122830](https://github.com/heldergaraujo2/Cortex/actions/runs/43645122830)
- **Resultado técnico do workflow:** `success`
- **Branch / commit:** `experiment/synthetic-neural-learning-smoke` / `c4660cce6230`
- **Atualizado pelo GitHub em:** `2026-11-14T215312Z` (UTC)
- **Relatórios:** [artifact #14133955882](https://github.com/heldergaraujo2/Cortex/actions/runs/43645122830/artifacts/14133955882)
- **Conexões analisadas:** 64.107
- **Frames iguais por direção:** True; **eventos de entrada iguais:** True
- **Gates numéricos:** `all_subtypes_share_winner`=False, `baseline_near_zero`=True, `biological_direction_selectivity_validated`=False, `held_out_physiological_reference_verified`=False, `independent_anatomical_alignment_verified`=False, `normalized_graph`=True, `numerical_finite_integrated`=True, `numerical_finite_traces`=True, `stimulus_equal_frame_counts`=True, `stimulus_equal_total_input_events`=True

| Subtipo | Direção preferida simulada | DSI descritivo |
| --- | --- | ---: |
| T4a | p_positive | 0.062691 |
| T4b | q_positive | 0.059942 |
| T4c | p_positive | 0.146457 |
| T4d | p_positive | 0.047260 |

**Limite científico:** sucesso da CI não prova seletividade direcional biológica. Calibração anatômica e comparação fisiológica independente continuam pendentes.
O histórico anterior permanece no link de cada execução e em seus artifacts.
<!-- T4-AUTO-END -->
