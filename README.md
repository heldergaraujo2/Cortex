# Cortex — Núcleo Artificial Inspirado no Connectoma da Mosca

**Objetivo:** construir, de forma incremental e verificável, um sistema de inteligência artificial cujo núcleo neural computacional seja inspirado na conectividade real do cérebro da mosca-da-fruta (*Drosophila melanogaster*), começando por circuitos pequenos e validados antes de escalar.

O projeto não pretende copiar um cérebro humano nem afirmar que um mapa de conexões, por si só, constitui uma mente. O connectoma fornece principalmente a estrutura das ligações; dinâmica neuronal, sinapses, entradas sensoriais, aprendizagem, memória, objetivos e interfaces computacionais precisam ser modelados e avaliados separadamente.

## Documentação central

- [Roadmap](docs/ROADMAP.md) — fases, marcos e critérios de conclusão.
- [Continuidade](docs/CONTINUIDADE.md) — estado atual, decisões, evidências, testes e instruções para retomar em outro chat.
- [Planejamento do projeto](docs/PLANEJAMENTO_DO_PROJETO.md) — visão, requisitos, arquitetura, método científico, riscos e estratégia de validação.

## Princípios obrigatórios

1. **Evidência antes de alegações:** distinguir CONFIRMADO, FORTEMENTE INDICADO, HIPÓTESE e DESCONHECIDO.
2. **Reprodutibilidade:** dados versionados por origem e snapshot, configurações explícitas, sementes aleatórias registradas e experimentos repetíveis.
3. **Começar pequeno:** primeiro um circuito real, pequeno, compreendido e testável; só depois ampliar.
4. **Separar estrutura de função:** conectividade biológica não é automaticamente dinâmica funcional.
5. **Aprendizagem mensurável:** estabelecer baselines e comparar ablações e controles.
6. **Escala responsável:** medir memória, tempo, custo computacional e fidelidade antes de aumentar o modelo.
7. **Documentação viva:** atualizar o arquivo docs/CONTINUIDADE.md a cada alteração relevante e manter roadmap/plano alinhados.
8. **Integridade do repositório:** nunca apagar, sobrescrever ou reestruturar dados existentes sem inspeção e justificativa; manter mudanças pequenas e testáveis.

## Fonte científica inicial

O projeto começará avaliando snapshots públicos do FlyWire/Codex. A escolha do dataset e versão deve ser registrada antes de importar dados. O dataset contém milhares de vezes mais detalhes do que um protótipo precisa; os dados brutos grandes não devem ser commitados sem necessidade e sem verificar licença, citação, tamanho e política de armazenamento.

- FlyWire Codex: https://codex.flywire.ai/
- FAQ e downloads do Codex: https://codex.flywire.ai/faq
- Artigo do connectoma cerebral adulto: https://www.nature.com/articles/s41586-024-07558-y
- Tutoriais de acesso: https://github.com/seung-lab/FlyConnectome

## Arquitetura coletiva aprovada como hipótese

O projeto seguirá uma arquitetura híbrida que poderá executar **quatro instâncias completas e independentes** do connectoma escolhido, cada uma com uma especialização experimental. A configuração inicial prevê um cérebro coordenador e três instâncias especializadas em percepção, aprendizagem e ação. As quatro instâncias partilharão uma memória coletiva versionada, mantendo estados neurais individuais separados. Um orquestrador convencional cuidará de contratos, registos, timeouts e recuperação; não será um quinto cérebro.

Esta arquitetura é uma decisão de planeamento, ainda não implementada nem validada. Os ganhos de cooperação, especialização e memória partilhada precisam de ser demonstrados por comparação com baselines. A anatomia real e os circuitos selecionados poderão exigir ajustes nos papéis.

- [Arquitetura híbrida e Cortex coletivo](docs/ARCHITECTURE.md)
- [Contratos técnicos iniciais](docs/CONTRATOS_TECNICOS.md) — contratos de mensagens C1–C4 e requisitos da memória/simulador.
- [Fontes científicas e dataset](docs/SCIENTIFIC_SOURCES.md) — comparação inicial BANC/FAFB, proveniência e licença.
- [Fase 2 — circuito inicial](docs/FASE_2_CIRCUITO_INICIAL.md) — via ON L1→Mi1/Tm3→T4, tarefa piloto, baselines e limites.
- [Manifesto do piloto FAFB v783](data/manifests/fafb_v783_t4_on_pilot.json) — seleção reprodutível sem dados brutos ou IDs inventados.

## Estado atual

O repositório contém um pipeline reproduzível para o subgrafo piloto do FlyWire FAFB v783, validação estrutural e espacial, um baseline determinístico rate-based e diagnósticos de frentes espaço-temporais sobre a malha medular p/q. Os workflows GitHub Actions executam testes e experimentos reais ME_L/ME_R; a última linha de base documentada aprovou 61 testes em Python 3.11, 3.12 e 3.13.

A auditoria e a importação estrutural real da Fase 7 preservaram 53.284 linhas de conexão candidatas para T4, incluindo 7.028 IDs pré-sinápticos e 6.236 IDs T4. O produto `neurons.csv.gz` cobre todos os 7.028 IDs; 50.630 linhas têm previsão `nt_type` não vazia, 2.654 vazias e nenhuma divergência interna com o rótulo da aresta. Isso é consistência de previsões Codex, não validação biológica; o dump não inclui `nt_type_verified`. O protótipo sintético T4 é separado do baseline v0. Cortex CI #155 aprovou 88 testes em Python 3.11–3.13. Próximo passo: perfis por T4-alvo e mapeamento espacial dos candidatos. Relatórios: `docs/FASE_7_AUDITORIA_INPUTS_T4.md` e `docs/FASE_7_MODELO_T4_ASSINADO.md`.

**Limites atuais:** o modelo não representa ainda inibição fisiológica calibrada, atrasos biológicos, dinâmica de membrana, plasticidade, aprendizagem ou seletividade direcional validada. Os índices de assimetria dos experimentos anteriores são diagnósticos de engenharia, não DSI biológico. `syn_count` é uma medida estrutural e `nt_type` não deve ser convertido em sinal funcional sem validação da semântica e da cobertura.

O fluxo atual é GitHub-first. A validação local Windows e o profiling no hardware do responsável foram adiados até que sejam tecnicamente necessários. A branch experimental `data/fafb-v783-inputs` permanece separada de `main`; não integrar sem revisão e decisão explícita.
