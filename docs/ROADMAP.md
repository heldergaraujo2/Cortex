# Roadmap do Cortex

**Versão:** 1.0 inicial  
**Data de criação:** 2026-10-28  
**Status global:** Fase 1 — bootstrap remoto concluído; Fase 2 — seleção do circuito e desenho experimental concluídos; Fase 3 — aquisição e validação dos dados reais por iniciar (gate de acesso aos produtos).  
**Princípio:** uma fase só é considerada concluída quando seus critérios de saída foram verificados e registrados em CONTINUIDADE.md.

## Intenção do projeto

Desenvolver um sistema de IA experimental com um núcleo computacional neural inspirado no connectoma real da mosca-da-fruta, complementado por módulos explícitos de percepção, memória, aprendizagem, planeamento, decisão e interação. O objetivo é investigar quanto comportamento adaptativo útil pode emergir de uma arquitetura neural conectômica quando fornecemos dinâmica, sinais de entrada, regras de plasticidade, tarefas e critérios de avaliação bem definidos.

O projeto não deve afirmar que reproduz a consciência, a inteligência geral ou o funcionamento integral do cérebro da mosca sem evidências específicas. O mapa de conexões é uma base anatômica, não um simulador biológico completo.

## Regras de execução do roadmap

- Não saltar etapas de validação para acelerar a implementação.
- Não escolher um modelo neuronal complexo antes de construir baselines simples e documentados.
- Não carregar o connectoma inteiro antes de medir custo e validar um circuito reduzido.
- Não misturar dados brutos, dados processados, parâmetros inferidos e resultados experimentais sem rastreabilidade.
- Não usar um LLM convencional como núcleo neural inicial. Ferramentas externas ou LLMs podem ser avaliados mais tarde como comparação ou interface opcional, sempre separados do núcleo e identificados nos resultados.
- Não considerar uma demonstração visual como prova de aprendizagem.
- Não marcar uma tarefa como concluída apenas porque o código foi escrito; executar testes e registrar resultados.
- Atualizar este roadmap quando a sequência, os marcos ou os critérios mudarem; atualizar CONTINUIDADE.md após toda alteração relevante.

## Fase 0 — Fundação documental e governança

**Estado:** documentação inicial criada; auditoria técnica pendente.

### Objetivos
- Definir a missão, os limites científicos e a estratégia incremental.
- Criar documentos persistentes para que novos chats retomem o trabalho sem depender de contexto conversacional.
- Definir evidências, validação, segurança dos dados e gestão de mudanças.

### Entregáveis
- README com visão e links para documentação.
- Roadmap por fases.
- Arquivo de continuidade com estado, decisões, evidências, testes e próximo passo.
- Planejamento detalhado com requisitos, arquitetura e riscos.

### Critérios de saída
- Todos os documentos estão no repositório.
- A continuidade identifica explicitamente o que foi e o que não foi verificado.
- O responsável confirma que a direção do projeto está alinhada.

## Fase 1 — Auditoria remota, bootstrap reproduzível e diagnóstico seguro

**Estado:** bootstrap remoto implementado; 11 testes passaram num ambiente isolado Python 3.13 e instalação editável do pacote passou. Workflow CI configurado para Python 3.11–3.13; execução do workflow no GitHub não pôde ser confirmada pelo conector disponível. A medição do PC fica adiada até ser necessária para profiling ou importação de dados.

### Objetivos
- Auditar o estado visível do repositório remoto sem presumir estado local.
- Estabelecer estrutura Python mínima, dependências de desenvolvimento e testes reproduzíveis.
- Criar um diagnóstico local de leitura apenas para recolher capacidades quando houver necessidade real de execução no PC.
- Definir a regra de não guardar dados científicos brutos nem artefactos grandes no Git.
- Formalizar contratos iniciais entre as quatro instâncias e o estado de evidência.

### Atividades concluídas no remoto
1. Confirmar repositório público, branch padrão `main` e permissão de escrita via integração GitHub.
2. Confirmar que antes do scaffold não existiam `pyproject.toml`, `.gitignore`, pacote Python, testes ou workflow CI.
3. Criar configuração Python compatível com 3.11–3.13, pacote `cortex`, testes e GitHub Actions.
4. Criar contratos tipados iniciais para C1–C4, tarefas, resultados e estado epistémico.
5. Criar diagnóstico local que não altera o ambiente nem grava ficheiros.
6. Definir exclusões de dados brutos, bases processadas, checkpoints e resultados gerados no `.gitignore`.

### Atividades pendentes para a etapa de dados/execução
- Verificar o resultado real do workflow CI e corrigir falhas caso existam.
- Quando o primeiro teste com dados reais ou profiling for necessário, executar `python -m cortex.diagnostics` no PC e registar sistema, Python, Git, CPU, RAM, espaço livre e GPU disponível.
- Não confundir o diagnóstico remoto de GitHub Actions com as capacidades do PC do responsável.

### Entregáveis
- `pyproject.toml` e `.gitignore`.
- Pacote `cortex` e testes iniciais.
- Workflow `.github/workflows/tests.yml`.
- `docs/CONTRATOS_TECNICOS.md`.
- Diagnóstico seguro `cortex.diagnostics`.
- Relatório remoto de auditoria e registo explícito das incógnitas locais em `docs/CONTINUIDADE.md`.

### Critérios de saída do gate remoto
- Instalação editável limpa e testes passam num ambiente isolado reproduzível.
- Workflow CI está configurado para verificar adicionalmente Python 3.11, 3.12 e 3.13; o estado remoto deve ser confirmado quando houver acesso ao painel de execuções.
- Contratos rejeitam campos inválidos e preservam origem/estado de evidência.
- Dados grandes e configurações locais não são incluídos por omissão.
- A continuidade separa claramente factos remotos de factos locais não verificados.

**Nota de escopo:** o inventário físico do PC não bloqueia a construção documental nem os testes de contrato. Será obrigatório antes de decisões de escala e profiling, não será inventado nesta fase.

## Fase 2 — Revisão científica e escolha do dataset

### Objetivos
- Confirmar ou rejeitar a escolha provisória documentada em `docs/SCIENTIFIC_SOURCES.md`.
- Selecionar dataset, snapshot e produtos de download com origem verificável.
- Entender formato, cobertura, critérios de filtragem, campos, unidades, limiar de conexão e licenças/citações.
- Distinguir número de neurónios, sinapses individuais e pares de neurónios conectados.

### Atividades
1. Consultar o portal FlyWire Codex e sua FAQ oficial.
2. Comparar os datasets disponíveis, incluindo FAFB e BANC, sem presumir que sejam intercambiáveis.
3. Ler os artigos científicos primários relevantes e registrar as limitações.
4. Identificar os arquivos compactos de neurônios, conexões, classificações e neurotransmissores disponíveis.
5. Registrar data de acesso, versão/snapshot, URL de origem, hash local quando baixado, tamanho e citação.
6. Criar uma ficha de proveniência e um manifesto de dados.
7. Escolher um circuito de interesse pequeno com anotação suficiente para validar a cadeia de processamento.

### Entregáveis
- docs/SCIENTIFIC_SOURCES.md.
- Manifesto de dataset.
- Decisão fundamentada sobre dataset e snapshot.
- Lista de incógnitas científicas e hipóteses.

### Critérios de saída
- A origem e versão dos dados são reproduzíveis.
- Os formatos e os campos usados estão documentados.
- O circuito inicial pode ser delimitado com regras explícitas.
- Dados brutos grandes não são commitados inadvertidamente.

## Fase 3 — Importação, normalização e integridade do connectoma

### Objetivos
- Construir um pipeline de importação robusto e testável, independente do simulador.
- Converter os dados para uma representação interna eficiente e rastreável.

### Atividades
1. Criar importadores para os formatos escolhidos.
2. Validar colunas obrigatórias, tipos, valores ausentes, IDs, duplicatas e relações pré/pós-sinápticas.
3. Definir como agregar ligações que aparecem em múltiplas regiões.
4. Preservar contagens de sinapses, regiões, tipo de neurotransmissor e metadados quando disponíveis.
5. Definir limiar de conexão como parâmetro explícito; não eliminar informação silenciosamente.
6. Gerar relatórios de integridade e estatísticas de grafo.
7. Criar pequenos fixtures sintéticos para testes sem distribuir o dataset completo.
8. Documentar transformações e permitir que sejam repetidas.

### Entregáveis
- Módulo de importação.
- Modelo de dados interno.
- Relatório de validação.
- Testes unitários para dados válidos e inválidos.
- Manifesto com hashes e versões.

### Critérios de saída
- Os dados importados correspondem às fontes de entrada dentro das regras de transformação documentadas.
- Os testes detectam corrupção, duplicatas e IDs inconsistentes.
- Uma amostra pequena é reprocessável de ponta a ponta.

## Fase 4 — Grafo conectômico mínimo e análise estrutural

### Objetivos
- Representar neurônios como nós e conexões dirigidas como arestas.
- Inspecionar topologia antes de atribuir dinâmica neuronal.

### Atividades
- Implementar consultas a vizinhos de entrada/saída, graus, caminhos e subgrafos.
- Medir conectividade, componentes, distribuição de graus e motivos simples.
- Validar estatísticas selecionadas contra fontes ou cálculos independentes.
- Visualizar circuitos pequenos com rótulos e proveniência.
- Comparar limiares de conectividade sem misturar resultados de configurações diferentes.

### Entregáveis
- Representação do grafo.
- Ferramentas de extração de subgrafos.
- Relatórios estruturais.
- Testes de invariantes do grafo.

### Critérios de saída
- Direção das conexões é preservada.
- Estatísticas reproduzíveis em dataset de teste.
- Subgrafos podem ser extraídos por regras registradas.

## Fase 5 — Primeiro circuito biologicamente ancorado

### Objetivos
- Escolher um circuito pequeno que possa ser compreendido e testado.
- Construir uma representação funcional mínima, sem alegar que equivale ao comportamento biológico real.

### Atividades
1. Selecionar um circuito sensorial, de processamento local ou reflexo com literatura e anotações disponíveis.
2. Documentar neurônios, conexões, neurotransmissores e incertezas.
3. Definir entradas e saídas computacionais observáveis.
4. Criar uma implementação de referência pequena.
5. Criar casos de teste determinísticos e casos de referência.
6. Definir quais propriedades são biológicas e quais são abstrações de engenharia.

### Entregáveis
- Documento do circuito.
- Fixture conectômico pequeno.
- Testes de importação e estrutura.
- Especificação da tarefa de validação.

### Critérios de saída
- Outro desenvolvedor consegue reproduzir o subgrafo e compreender a tarefa.
- O circuito tem uma entrada e uma saída mensuráveis.
- Hipóteses e abstrações são explícitas.

## Fase 6 — Modelos de neurônios e sinapses

### Objetivos
- Implementar dinâmica temporal para neurônios e transmissão sináptica.
- Escolher complexidade proporcional à pergunta científica e ao orçamento computacional.

### Atividades
1. Implementar um baseline simples, como neurônios de taxa ou um modelo de disparos simplificado.
2. Avaliar depois modelos de neurônios com disparos, por exemplo Integrate-and-Fire, se fizer sentido.
3. Representar atraso, sinal excitatório/inibitório e pesos quando houver base para isso.
4. Separar propriedades medidas de parâmetros inferidos ou escolhidos por conveniência.
5. Definir integração temporal, unidades, estabilidade numérica e condições iniciais.
6. Criar testes para neurônio isolado, sinapse isolada e pequenas redes.
7. Comparar precisão, velocidade e custo de memória.

### Entregáveis
- Interface de neurônio.
- Interface sináptica.
- Simulador temporal inicial.
- Testes numéricos e documentação das equações.

### Critérios de saída
- Comportamento básico estável e reproduzível.
- Resultados compatíveis com as equações implementadas.
- Parâmetros e unidades documentados.
- Nenhuma alegação de fidelidade biológica sem validação correspondente.

## Fase 7 — Simulador do circuito e baseline funcional

### Objetivos
- Executar o circuito selecionado ao longo do tempo.
- Estabelecer uma referência antes de introduzir aprendizagem.

### Atividades
- Integrar grafo, neurônios, sinapses e estímulos.
- Registrar atividade neuronal, latência, saídas, eventos e métricas.
- Controlar sementes e configurações.
- Criar simulações repetíveis e relatórios automáticos.
- Testar ausência de estímulo, estímulo esperado, estímulo inesperado e perturbações.
- Comparar o circuito real com versões de controle: conexões removidas, pesos aleatorizados ou topologia de comparação.

### Entregáveis
- Comando de execução de experimento.
- Formato de resultados.
- Baseline funcional documentado.
- Testes de determinismo e regressão.

### Critérios de saída
- A mesma configuração produz resultados reproduzíveis dentro da tolerância definida.
- Métricas e condições experimentais são registradas.
- O circuito supera ou caracteriza baselines de forma quantificada.

## Fase 8 — Aprendizagem e plasticidade controladas

### Objetivos
- Investigar adaptação mensurável sem confundir mudança de parâmetro com inteligência geral.
- Separar plasticidade local inspirada biologicamente de métodos de otimização usados como controle.

### Atividades
1. Definir tarefa simples, recompensa/erro observável e métrica de sucesso.
2. Implementar uma regra de plasticidade por vez.
3. Comparar com ausência de aprendizagem e com baselines não conectômicos.
4. Medir desempenho antes, durante e depois do treino.
5. Avaliar retenção, generalização limitada, esquecimento e estabilidade.
6. Registrar hiperparâmetros, sementes, duração e custo.
7. Manter possibilidade de desligar aprendizagem e restaurar parâmetros experimentais.

### Entregáveis
- Módulo de plasticidade.
- Protocolo de treino.
- Comparação experimental.
- Relatório de limites e resultados negativos.

### Critérios de saída
- A melhoria é mensurável em dados de teste não usados no ajuste.
- Há controles adequados e repetições suficientes para interpretar o resultado.
- O estado treinado pode ser salvo e recarregado.
- Nenhuma conclusão extrapola os experimentos realizados.

## Fase 9 — Memória, contexto e aprendizagem de tarefas

### Objetivos
- Investigar mecanismos de estado persistente e memória da tarefa sem confundir armazenamento externo com memória neural emergente.

### Atividades
- Distinguir estado dinâmico temporário, pesos/plasticidade persistentes e memória externa explícita.
- Criar testes de codificação, recuperação, interferência e retenção.
- Definir formato de checkpoint versionado e migrações.
- Comparar o comportamento com e sem cada tipo de memória.
- Garantir que cada resultado indique qual componente foi responsável.

### Entregáveis
- Contratos de memória.
- Persistência e carregamento versionados.
- Testes de continuidade de estado.
- Experimentos de retenção.

### Critérios de saída
- O sistema recupera estado de forma consistente.
- A memória melhora ou altera métricas específicas de forma mensurável.
- A proveniência de cada informação persistente é rastreável.

## Fase 10 — Módulos cognitivos e integração híbrida

### Objetivos
- Integrar, quando justificado por evidências, módulos de percepção, memória, planeamento, decisão e execução em torno do núcleo neural.
- Manter separação arquitetural entre núcleo neural, ferramentas convencionais e interfaces externas.

### Atividades
- Definir contratos de entrada/saída e limites entre módulos.
- Introduzir um módulo por vez, com teste isolado e ablação.
- Avaliar ferramentas algorítmicas convencionais como baseline.
- Se um LLM ou agente externo for avaliado, mantê-lo opcional, isolado e claramente identificado; não atribuir suas capacidades ao núcleo conectômico.
- Definir políticas de permissão para qualquer ação externa.
- Registrar cada intervenção e resultado.

### Entregáveis
- Interfaces modulares.
- Plano de integração.
- Testes de contrato.
- Comparação com e sem módulos auxiliares.

### Critérios de saída
- Cada módulo pode ser ligado/desligado sem invalidar a avaliação.
- É possível atribuir as capacidades observadas aos componentes testados.
- A integração não compromete reprodutibilidade nem segurança.

## Fase 11 — Escala, desempenho e otimização

### Objetivos
- Escalar do circuito validado para circuitos maiores apenas quando a evidência justificar.
- Controlar uso de RAM, VRAM, armazenamento e tempo.

### Atividades
- Fazer profiling antes de otimizar.
- Comparar estruturas de dados esparsas, processamento em lotes e execução paralela.
- Medir custo por neurônio, sinapse, passo temporal e segundo simulado.
- Definir metas de desempenho por hardware.
- Estabelecer checkpoints e retomada de experimentos interrompidos.
- Validar que otimizações preservam resultados dentro de tolerâncias.

### Entregáveis
- Relatório de desempenho.
- Plano de escala.
- Testes de equivalência antes/depois de otimizações.
- Estimativa de custo por tamanho do circuito.

### Critérios de saída
- A escala alvo cabe no orçamento declarado.
- Os resultados continuam corretos após otimizações.
- Limites e gargalos estão quantificados.

## Fase 12 — Avaliação científica, robustez e replicação

### Objetivos
- Avaliar a qualidade das conclusões e a robustez do sistema.
- Reduzir o risco de resultados ocasionais, sobreajuste ou interpretações indevidas.

### Atividades
- Repetir experimentos com múltiplas sementes quando aplicável.
- Separar dados de desenvolvimento e teste.
- Fazer ablações e comparações com baselines relevantes.
- Documentar resultados negativos e falhas.
- Comparar propriedades selecionadas com literatura, sem alegar equivalência total.
- Verificar reprodutibilidade em ambiente limpo.
- Auditar dependências, licenças e documentação.

### Entregáveis
- Relatório de avaliação.
- Experimentos reproduzíveis.
- Matriz de alegações versus evidências.
- Limitações conhecidas.

### Critérios de saída
- Resultados principais reproduzidos.
- Métricas e limitações transparentes.
- Conclusões sustentadas pelos dados.

## Fase 13 — Ferramentas de desenvolvimento e interface

### Objetivos
- Criar uma interface de experimentação útil depois de estabilizar o núcleo.
- Não deixar a interface mascarar limitações do motor neural.

### Atividades
- CLI para importar, validar, simular, treinar e avaliar.
- Visualização de subgrafos e séries temporais.
- Relatórios exportáveis com configuração e proveniência.
- Interface opcional para tarefas e observação.
- Documentação de instalação e exemplos reproduzíveis.

### Critérios de saída
- Fluxos principais podem ser executados sem edição manual de código.
- Cada visualização liga-se a um experimento e configuração identificáveis.
- Interface não executa ações perigosas por padrão.

## Fase 14 — Release experimental e manutenção

### Objetivos
- Produzir uma versão experimental clara, reproduzível e honesta sobre o que faz.
- Manter continuidade do trabalho entre pessoas, máquinas e chats.

### Atividades
- Revisar documentação, testes, dependências e licenças.
- Publicar exemplos pequenos que não dependam de dados grandes privados.
- Versionar formatos de dados, checkpoints e resultados.
- Criar notas de versão e plano para a próxima iteração.
- Atualizar CONTINUIDADE.md após cada mudança relevante e antes de encerrar uma sessão de trabalho.

### Critérios de saída
- Instalação e experimento de demonstração documentados.
- Limitações e requisitos de hardware publicados.
- Um novo colaborador consegue reproduzir o experimento inicial.

## Critérios transversais de conclusão

Cada tarefa de engenharia deve registrar:
- objetivo e hipótese;
- arquivos alterados;
- origem dos dados;
- comandos executados;
- testes executados e resultado real;
- limitações e falhas;
- evidência classificada;
- commit ou referência exata, quando disponível;
- impacto sobre o roadmap;
- atualização da continuidade;
- próximo passo único e verificável.

## Referências científicas e técnicas iniciais

- FlyWire Codex: https://codex.flywire.ai/
- FAQ oficial do Codex: https://codex.flywire.ai/faq
- Dorkenwald et al., “Neuronal wiring diagram of an adult brain”, Nature (2024): https://www.nature.com/articles/s41586-024-07558-y
- Tutoriais FlyConnectome: https://github.com/seung-lab/FlyConnectome


## Aditivo de arquitetura — quatro cérebros e memória coletiva (2026-10-28)

A arquitetura experimental passa a prever quatro instâncias completas do connectoma de referência, com estados neurais independentes e especializações por tarefa:
- C1: coordenação e consolidação;
- C2: percepção;
- C3: aprendizagem/plasticidade;
- C4: ação/comportamento.

As quatro instâncias consultarão uma memória coletiva versionada, com proveniência e gestão explícita de conflitos. O estado neural dinâmico e os parâmetros plásticos permanecem independentes inicialmente. Um orquestrador determinístico de software cuidará de contratos, registos, timeouts e recuperação, sem ser contado como cérebro adicional.

Esta decisão altera o desenho futuro das fases 9–11 e exige testes de memória partilhada, concorrência, coordenação, falha e ablação. Não antecipa a implementação: a Fase 1 (auditoria do ambiente) continua a ser o próximo passo, e qualquer escalada para quatro instâncias deve esperar por medições de custo e validação do simulador mínimo.

Critério de avaliação: comparar quatro instâncias isoladas, cooperação sem coordenador, cooperação com C1, e memória partilhada ligada/desligada. A hipótese de melhoria coletiva só será aceite se as métricas a sustentarem.


## Aditivo 2026-10-28 — Fase 2: circuito piloto selecionado documentalmente

A investigação de fontes públicas selecionou o núcleo exploratório da via ON de movimento `L1 → Mi1/Tm3 → T4` em FAFB v783. A literatura descreve Mi1 e Tm3 como entradas importantes para T4, mas também identifica entradas adicionais e incertezas sobre a operação funcional. O núcleo é deliberadamente parcial e não deve ser apresentado como reconstrução completa do circuito.

- Documento experimental: `docs/FASE_2_CIRCUITO_INICIAL.md`.
- Manifesto versionado: `data/manifests/fafb_v783_t4_on_pilot.json`.
- Especificação tipada e validação de metadados: `cortex/experiments/motion_t4.py`.
- Testes da especificação: `tests/test_motion_t4_spec.py`.
- Teste executado em ambiente temporário isolado: **3 passed in 0.05s**. O teste valida apenas a especificação de software, não os dados biológicos.

### Gate de dados que antecede o importador

O FAQ oficial confirma que os downloads em lote devem usar CSVs estáticos e fornece o exemplo oficial com `consolidated_cell_types` e `connections_princeton`. Também declara que conexões são dirigidas, podem ter várias linhas por neuropilo e que o limiar padrão FAFB é 5+ sinapses por par. A FAQ oficial atual descreve downloads estáticos públicos via `api/download` e `api/download_resource`; token CAVE/FlyWire é necessário para operações específicas ao vivo/protegidas. A acessibilidade concreta dos endpoints deve ser testada, sem presumir que downloads estáticos exijam token. Nenhum segredo foi pedido ou armazenado.

Assim, a seleção documental do circuito e o desenho da tarefa estão concluídos, mas a extração real continua bloqueada até os produtos exatos, cabeçalhos, tamanhos, licença por produto e correspondência espacial serem verificados. O motor não deve usar a métrica direcional como válida até ser demonstrado que a correspondência espacial está disponível. A fase seguinte começa com este gate de aquisição/validação, não com a implementação prematura da dinâmica.


### Fecho da Fase 2 — seleção e desenho experimental (2026-10-28)

**Estado:** concluída no âmbito de seleção e desenho, com gate de dados explicitamente bloqueado e transferido para a Fase 3.

Entregáveis concluídos:
- dataset/snapshot FAFB v783 selecionado;
- circuito exploratório reproduzível `L1 → Mi1/Tm3 → T4` definido por tipos e arestas dirigidas;
- tarefa sintética proposta com duas direções, flash estático e condição sem estímulo;
- métrica candidata, baselines, ablações e limitações documentadas;
- manifesto JSON, especificação tipada e testes adicionados;
- três testes da especificação passaram no ambiente temporário de validação.

Limite explícito: root IDs concretos, número real de células/arestas, cabeçalhos/tamanhos exatos dos produtos Codex e mapeamento espacial de colunas ainda não foram verificados. A FAQ oficial consultada descreve os downloads estáticos como públicos e reserva o token CAVE/FlyWire para operações específicas ao vivo/protegidas. A acessibilidade dos endpoints concretos ainda não foi confirmada neste ambiente. Não foi descarregado dado bruto.

A Fase 3 começa com a aquisição autorizada dos produtos mínimos, verificação dos metadados/licença/cabeçalhos e extração real do circuito. Se a correspondência espacial não estiver disponível no produto selecionado, a tarefa direcional deve ser reduzida a validação topológica até existir uma fonte adequada.
