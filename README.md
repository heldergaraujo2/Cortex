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

O repositório já contém um scaffold Python mínimo, contratos tipados para mensagens entre instâncias, testes unitários e workflow de CI para Python 3.11–3.13. Isso ainda não é um simulador neural: não existe importador de connectoma, dinâmica neuronal, plasticidade nem memória coletiva implementada.

O dataset selecionado para o primeiro protótipo é FlyWire FAFB v783 (cérebro adulto feminino completo, incluindo lobos ópticos; sem cordão nervoso), com licença pública CC BY-NC 4.0 e atribuição obrigatória. BANC v888 fica como possível extensão futura para circuitos cérebro–cordão nervoso. Nenhum dataset foi baixado; antes disso, serão verificados os metadados e os produtos concretos necessários para um circuito pequeno.

A auditoria do PC será feita quando a execução local for necessária para validar recursos reais; existe agora um diagnóstico de leitura apenas em `python -m cortex.diagnostics`, que não instala nada nem escreve arquivos.
