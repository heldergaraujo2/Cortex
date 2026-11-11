# Fase 7 — perfis estruturais por alvo T4

**Estado:** perfis estruturais reais por T4-alvo gerados e validados no GitHub. A geometria dos neurónios pré-sinápticos candidatos continua sem atribuição de coluna.

## 1. Execução

- Workflow: FAFB v783 Data Validation #128.
- Run: `41951942609`, sucesso.
- Artefato: `fafb-v783-validation-report`, ID `13381252165`.
- SHA-256 do ZIP: `7f4897d7ad44f4aecded8b5be3d2e42d06da0a1d340bd0cb0075669cc43bb760`.
- Relatório: `fafb_v783_t4_target_profiles.json`.
- CI geral #165: 95 testes aprovados em Python 3.11, 3.12 e 3.13.

## 2. Junção por identidade exata

O script `scripts/summarize_t4_target_profiles.py` junta as 53.284 arestas T4 importadas com `column_assignment.csv.gz` pelo `post_root_id` exato e verifica se o tipo T4 coincide.

| Métrica | Resultado |
|---|---:|
| T4-alvos distintos com pelo menos uma aresta candidata | 6.236 |
| T4-alvos com atribuição de coluna | 5.981 |
| T4-alvos sem atribuição de coluna | 255 |
| Linhas de aresta com alvo atribuído | 51.387 |
| Linhas de aresta com alvo sem atribuição | 1.897 |
| Linhas com divergência entre lado do neuropilo e hemisfério atribuído | 0 |
| Grupos agregados por T4, hemisfério, input, neuropilo e `nt_type` | 221 |
| Perfis individuais por T4-alvo | 6.236 |

A tabela completa de atribuições contém 5.985 IDs T4 atribuídos; quatro desses IDs não aparecem como alvo no subgrafo candidato. Por isso o número de alvos candidatos atribuídos é 5.981.

### Cobertura entre os T4-alvos com arestas candidatas

| Subtipo | Alvos candidatos | Atribuídos | Não atribuídos | Cobertura |
|---|---:|---:|---:|---:|
| T4a | 1.456 | 1.440 | 16 | 98,901% |
| T4b | 1.506 | 1.492 | 14 | 99,070% |
| T4c | 1.705 | 1.551 | 154 | 90,968% |
| T4d | 1.569 | 1.498 | 71 | 95,475% |

A ausência de divergências de hemisfério é uma validação estrutural útil: para todas as linhas cujo neuropilo tem sufixo `_L` ou `_R`, o lado coincide com o hemisfério da atribuição do T4-alvo. Nenhuma linha foi descartada por essa verificação.

## 3. Soma estrutural de syn_count por subtipo T4

Valores abaixo agregados apenas sobre neuropilos ME_L e ME_R e por tipo pré-sináptico. São somas de contagens estruturais, não pesos funcionais nem eficácia sináptica.

| T4 | C3 | CT1 | Mi1 | Mi4 | Mi9 | Tm3 | TmY15 |
|---|---:|---:|---:|---:|---:|---:|---:|
| T4a | 2.955 | 20.273 | 84.252 | 9.022 | 12.823 | 20.288 | 8.390 |
| T4b | 2.418 | 17.176 | 69.743 | 10.102 | 11.686 | 21.356 | 8.038 |
| T4c | 817 | 17.016 | 83.557 | 7.971 | 12.533 | 20.509 | 6.985 |
| T4d | 1.111 | 16.923 | 70.700 | 5.508 | 9.746 | 17.336 | 5.125 |

O artefato contém os perfis por root ID, incluindo coluna, hemisfério, p/q, x/y e grupos de inputs. O código preserva p/q e x/y sem inferir uma transformação retinal ou direção visual.

## 4. Limite espacial remanescente

O join resolveu a localização do alvo T4, mas não a localização dos 7.028 neurónios pré-sinápticos candidatos. A tabela `column_assignment.csv.gz` contém atribuições para L1, Mi1, Tm3 e T4; não fornece colunas para Mi4, Mi9, C3, CT1 ou TmY15.

Consequentemente:
- é possível comparar a composição estrutural dos inputs por T4-alvo, subtipo e coluna;
- ainda não é possível calcular offsets espaciais reais das arborizações pré-sinápticas;
- não se deve inferir direção preferencial apenas com a posição do T4-alvo;
- nenhum sinal sináptico, atraso ou DSI biológico é atribuído neste relatório.

## 5. Próxima subetapa

1. Investigar se coordenadas FAFB e morfologia permitem mapear os candidatos pré-sinápticos a colunas de forma validada.
2. Procurar anotações independentes/curadas de neurotransmissores e receptores pós-sinápticos.
3. Construir uma matriz de conectividade por T4-alvo, input type e posição, mantendo rótulos incertos.
4. Só então integrar sinais e offsets ao modelo experimental e executar ablações por classe.
