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

## Estado inicial

O repositório foi informado pelo responsável como https://github.com/heldergaraujo2/Cortex.git. Na primeira inspeção via integração GitHub, a API informou que o repositório estava vazio. Portanto, os documentos iniciais estabelecem a direção do projeto, mas nenhum código de simulação, dataset, experimento ou teste funcional foi confirmado como existente.

A primeira fase de execução é auditar o estado real do repositório e do ambiente de desenvolvimento antes de implementar o núcleo.
