# Planejamento Técnico e Científico do Cortex

**Versão:** 1.0 inicial  
**Data:** 2026-10-28  
**Status:** plano inicial; decisões técnicas dependentes de auditoria, análise de dados e experimentos.  
**Documento relacionado:** docs/ROADMAP.md e docs/CONTINUIDADE.md.

## 1. Resumo executivo

Cortex é um projeto de pesquisa e engenharia para construir uma IA experimental cujo núcleo computacional seja inspirado na estrutura do sistema nervoso da mosca-da-fruta (*Drosophila melanogaster*). A base anatômica virá de dados públicos de connectoma, inicialmente investigando os datasets FlyWire disponibilizados via Codex. O sistema será construído de baixo para cima: dados, grafo, circuito pequeno, dinâmica neuronal, simulação, aprendizagem mensurável, memória e integração modular.

A ambição é desenvolver um sistema capaz de aprender e resolver tarefas concretas, sobretudo tarefas computacionais e de programação em fases posteriores, mas não se presume que a conectividade da mosca gere essas capacidades automaticamente. Cada capacidade deverá ser implementada, medida e atribuída aos componentes que realmente a produzem.

O objetivo não é copiar o cérebro humano. Estudos de outros sistemas nervosos podem informar hipóteses e modelos comparativos, mas a arquitetura inicial será ancorada no connectoma escolhido e em evidência publicada. Também não se presume que a mosca tenha uma arquitetura diretamente adequada a programação: a transferência para tarefas abstratas é uma hipótese de investigação, não um fato estabelecido.

## 2. Missão, visão e não-objetivos

### 2.1 Missão
Construir uma plataforma reprodutível para investigar como um grafo neural biologicamente informado, equipado com dinâmica, entradas, plasticidade e memória, pode realizar tarefas observáveis e aprender com experiência.

### 2.2 Visão de longo prazo
Uma arquitetura modular na qual um núcleo neural conectômico possa ser testado isoladamente e integrado, se os resultados justificarem, a módulos de percepção, memória explícita, planeamento, tomada de decisão e execução. O desempenho do núcleo e o desempenho da arquitetura integrada serão avaliados separadamente.

### 2.3 Não-objetivos iniciais
- Não afirmar que o projeto é uma réplica funcional completa do cérebro da mosca.
- Não afirmar consciência, senciência, emoções humanas ou inteligência geral.
- Não começar pela simulação de todos os neurônios do dataset completo.
- Não tratar o número de neurônios como medida suficiente de inteligência.
- Não assumir que uma conexão anatômica determina sozinha o sinal, peso, atraso ou dinâmica.
- Não usar um LLM como núcleo neural inicial, pois isso impediria medir claramente o que o sistema conectômico aprende por si.
- Não introduzir autonomia irrestrita, execução de código arbitrário ou acesso não controlado ao sistema operacional.
- Não prometer desempenho de programação antes de testes comparativos.
- Não misturar o projeto Cortex com o projeto Lúmen ou outros repositórios; qualquer integração futura será uma decisão separada e explícita.

## 3. Princípios de investigação

1. **Rastreabilidade:** toda conclusão deve apontar para dados, código, configuração e experimento.
2. **Separação entre fatos e hipóteses:** usar as categorias CONFIRMADO, FORTEMENTE INDICADO, HIPÓTESE e DESCONHECIDO.
3. **Incrementalidade:** avançar por circuitos e tarefas pequenas.
4. **Baselines:** comparar com controles simples antes de declarar sucesso.
5. **Ablation first:** desligar ou perturbar componentes para identificar o que realmente contribui.
6. **Reprodutibilidade:** fixar versões, sementes, parâmetros e origem dos dados.
7. **Simplicidade inicial:** escolher o modelo mais simples que permita responder à pergunta da fase.
8. **Resultados negativos são resultados:** não ocultar falhas, ausência de aprendizagem ou desempenho inferior.
9. **Dados científicos não são automaticamente livres de obrigações:** registrar citação, condições de uso e proveniência.
10. **Segurança operacional:** simulador offline por padrão; sem execução externa não autorizada.

## 4. Evidência e linguagem de conclusão

Cada afirmação relevante deve receber uma categoria:

- **CONFIRMADO:** verificado diretamente em código, dados, teste reproduzido ou fonte primária.
- **FORTEMENTE INDICADO:** apoiado por múltiplas evidências relevantes, mas não verificado integralmente no ambiente atual.
- **HIPÓTESE:** proposta que precisa ser testada.
- **DESCONHECIDO:** falta evidência suficiente.

Exemplo: “o dataset contém uma tabela de conexões dirigidas” pode ser confirmado após inspeção do arquivo e esquema. “O circuito aprende uma tarefa” só pode ser confirmado após treino, teste separado, baseline e resultados reproduzidos. “A arquitetura poderá aprender programação” permanece hipótese até existirem experimentos que o sustentem.

## 5. Fundamento científico: connectoma não é simulador

Um connectoma é um mapa de elementos neurais e suas conexões. Um dataset pode incluir neurônios, pares pré/pós-sinápticos, contagens de sinapses, regiões, previsões de neurotransmissores e anotações. Isso não fornece automaticamente todos os parâmetros necessários para simular a atividade de um cérebro.

Para uma simulação funcional ainda são necessárias decisões ou evidências sobre:
- modelo de dinâmica de cada neurônio;
- transmissão e sinal sináptico;
- pesos e significado das contagens de sinapses;
- atraso de transmissão;
- tipos excitatórios/inibitórios e incerteza das anotações;
- estados iniciais e condições de contorno;
- entradas externas e significado dos estímulos;
- saídas e como interpretá-las;
- plasticidade e regras de aprendizagem;
- escalas temporais e integração numérica;
- validação contra resultados biológicos ou tarefas observáveis.

Quando esses parâmetros não estiverem disponíveis, o código deve rotulá-los como hipóteses ou escolhas de engenharia, não como dados biológicos confirmados.

## 6. Fontes de dados e estratégia de seleção

### 6.1 Fonte inicial
FlyWire Codex e suas versões estáticas são o ponto inicial de investigação. A FAQ do Codex recomenda downloads estáticos para análise em lote e diferencia snapshots consolidados de consultas live ao sistema CAVE.

Links de referência:
- https://codex.flywire.ai/
- https://codex.flywire.ai/faq
- https://www.nature.com/articles/s41586-024-07558-y
- https://github.com/seung-lab/FlyConnectome
- https://doi.org/10.5281/zenodo.10676866

### 6.2 Seleção de dataset
A seleção não será decidida apenas pelo maior número de neurônios. Avaliar:
- se o dataset cobre cérebro ou sistema nervoso central mais amplo;
- versão/snapshot e data;
- cobertura e qualidade das anotações;
- acesso a tabelas de conexões, neurônios, classes e neurotransmissores;
- limiares aplicados às conexões;
- formatos e tamanho dos arquivos;
- compatibilidade com o circuito escolhido;
- documentação científica e requisitos de citação.

### 6.3 Manifesto de dados
Para cada arquivo de origem, registrar:
- nome lógico e caminho local;
- URL e projeto de origem;
- versão/snapshot;
- data de download;
- tamanho em bytes;
- hash SHA-256 quando o arquivo estiver disponível localmente;
- formato e codificação;
- esquema de colunas;
- licença, termos e citação;
- transformações aplicadas;
- hash e versão dos produtos processados;
- limitações conhecidas.

### 6.4 Política de armazenamento
- Código, manifestos, documentação, scripts de download e fixtures pequenos podem ficar no Git.
- Dados brutos grandes, meshes, volumes e dumps completos não serão adicionados ao Git sem uma decisão explícita baseada em tamanho, licença e utilidade.
- Dados derivados devem ser reconstruíveis por scripts quando possível.
- Dados locais, caches e checkpoints devem ser ignorados por regras claras, mas nunca adicionar regras de exclusão sem verificar se escondem arquivos que precisam ser versionados.
- Não fazer scraping intensivo de interfaces web quando houver arquivos estáticos oficiais.

## 7. Arquitetura lógica proposta

A arquitetura é uma hipótese inicial sujeita a auditoria e validação. Ela deve permanecer modular para permitir comparar abordagens.

### 7.1 Camada de dados
Responsável por importar, validar e normalizar os arquivos de origem.
- adaptadores de formato;
- manifesto e proveniência;
- validação de esquema;
- transformações reprodutíveis;
- armazenamento de dados processados.

### 7.2 Camada conectômica
Representa neurônios como nós e ligações dirigidas como arestas.
- IDs estáveis;
- metadados neuronais;
- contagem de sinapses;
- regiões;
- tipo de neurotransmissor e confiança, quando disponível;
- filtros e limiares explícitos;
- extração de subgrafos.

### 7.3 Camada de dinâmica
Simula o estado neuronal no tempo.
- interface comum de neurônio;
- interface de sinapse;
- propagação de sinais;
- integração temporal;
- entradas e saídas;
- monitorização e registo de atividade.

### 7.4 Camada de plasticidade
Permite modificar parâmetros durante tarefas controladas.
- regras de aprendizagem intercambiáveis;
- parâmetros e estado versionados;
- mecanismos de congelamento;
- comparação com controle sem aprendizagem;
- registo da história de treino.

### 7.5 Camada de memória
Separar conceitos diferentes:
- estado dinâmico transitório do simulador;
- pesos e parâmetros plásticos persistentes;
- memória explícita externa usada pela tarefa;
- checkpoints e metadados experimentais.
A existência de armazenamento externo não será descrita como memória neural emergente.

### 7.6 Camada de tarefa e ambiente
Define estímulos, ações, recompensas ou critérios de erro e condições de avaliação. Começar com ambientes determinísticos e simples. Qualquer tarefa deve ter especificação e métricas independentes da implementação.

### 7.7 Camada de avaliação
- baselines;
- métricas;
- testes e sementes;
- ablações;
- relatórios;
- comparação treino/teste;
- análise de falhas;
- custo computacional.

### 7.8 Interfaces e módulos auxiliares futuros
Percepção, planeamento, decisão, ferramentas de programação e interfaces externas só serão integrados depois de existir um baseline do núcleo. Cada integração deve ser opcional e permitir ablação. Capacidades de um módulo externo não podem ser atribuídas ao núcleo neural.

## 8. Plano de implementação técnica

### Etapa A — Projeto executável mínimo
- Definir versão de Python após auditoria.
- Criar ambiente isolado e dependências mínimas.
- Configurar formatação, lint e testes conforme a complexidade real.
- Criar comandos simples para teste e diagnóstico.
- Evitar instalar bibliotecas pesadas antes de existir necessidade comprovada.

### Etapa B — Modelo de dados
- Definir entidades Neuron, Connection e DatasetManifest, ou equivalentes simples.
- Validar IDs e direção pré/pós-sináptica.
- Definir regras para arestas duplicadas e múltiplas regiões.
- Preservar informação de origem.
- Escrever testes de esquema e integridade.

### Etapa C — Grafo e circuitos
- Implementar grafo dirigido esparso.
- Criar extração de subgrafo com filtros explícitos.
- Calcular métricas estruturais.
- Comparar resultados com cálculos independentes.
- Visualizar apenas subgrafos pequenos inicialmente.

### Etapa D — Dinâmica neural
- Escolher primeiro modelo pela simplicidade e observabilidade.
- Documentar equações, unidades e parâmetros.
- Implementar integração temporal estável.
- Testar neurônio e sinapse isoladamente.
- Implementar o circuito escolhido com entradas e saídas observáveis.

### Etapa E — Aprendizagem
- Definir uma tarefa pequena e mensurável.
- Criar baseline sem plasticidade.
- Introduzir uma regra de aprendizagem por vez.
- Avaliar em amostras não usadas para ajuste.
- Registar convergência, falhas, estabilidade e retenção.

### Etapa F — Memória e tarefas sequenciais
- Definir o que precisa persistir.
- Implementar checkpoint versionado.
- Testar recuperação após reinício.
- Medir retenção e interferência em tarefas.
- Comparar com e sem memória explícita.

### Etapa G — Expansão e integração
- Selecionar circuito maior apenas após profiling.
- Medir custo por passo de simulação.
- Introduzir módulos auxiliares individualmente.
- Fazer ablações para cada módulo.
- Preservar resultados do núcleo isolado como referência.

## 9. Estratégia de avaliação

Nenhuma única métrica comprova inteligência. Cada experimento deve definir previamente uma pergunta e um conjunto de critérios.

### Métricas possíveis
- taxa de acerto ou erro na tarefa;
- recompensa acumulada, quando aplicável;
- tempo até resposta;
- estabilidade temporal;
- número de passos até convergência;
- retenção depois de intervalo ou reinicialização;
- generalização para condições não vistas;
- sensibilidade a ruído e perturbações;
- custo de RAM/VRAM;
- tempo de execução e throughput;
- variação entre sementes;
- diferença em relação a baselines.

### Baselines e controles
- saída aleatória ou política simples;
- circuito sem aprendizagem;
- circuito com pesos aleatorizados;
- circuito com arestas removidas ou perturbadas;
- circuito de topologia alternativa, quando viável;
- modelo convencional simples para a mesma tarefa;
- módulo auxiliar desligado versus ligado.

### Requisitos para afirmar aprendizagem
1. Definir previamente a métrica.
2. Separar treino e avaliação.
3. Executar repetições suficientes para medir variabilidade.
4. Comparar com controle sem aprendizagem.
5. Registrar configuração e sementes.
6. Mostrar que a diferença não é apenas efeito de vazamento, memorização trivial ou mudança de métrica.
7. Publicar resultados negativos e limitações.

## 10. Engenharia de software e estrutura de diretórios

A estrutura abaixo é uma proposta, não uma descrição de arquivos já existentes. Confirmar a árvore real na Fase 1 antes de criar diretórios ou mover conteúdo.

    Cortex/
      README.md
      pyproject.toml
      .gitignore
      docs/
        ROADMAP.md
        CONTINUIDADE.md
        PLANEJAMENTO_DO_PROJETO.md
        SCIENTIFIC_SOURCES.md
        ARCHITECTURE.md
        DATA_POLICY.md
      src/
        cortex/
          __init__.py
          data/
          connectome/
          neurons/
          synapses/
          simulation/
          plasticity/
          memory/
          tasks/
          evaluation/
          cli/
      tests/
        unit/
        integration/
        fixtures/
      scripts/
      configs/
      data/
        raw/          # normalmente fora do Git
        processed/    # normalmente fora do Git
        manifests/    # metadados pequenos e versionáveis
      experiments/
        README.md
        configs/
        results/      # resultados volumosos podem ficar fora do Git
      artifacts/      # checkpoints, normalmente fora do Git

### Regras de organização
- Código de produção em src/cortex, com imports explícitos.
- Testes pequenos em tests/fixtures.
- Dados científicos grandes fora do Git por padrão.
- Cada experimento tem configuração, versão de código, semente e manifesto.
- Evitar scripts monolíticos.
- Evitar abstrações genéricas antes de existirem dois casos reais que as justifiquem.
- Alterações de esquema de dados devem ter versão e estratégia de compatibilidade.

## 11. Dependências e tecnologias

A escolha final das bibliotecas depende da auditoria e de um protótipo medido. Possíveis categorias:
- NumPy/SciPy para operações numéricas;
- bibliotecas de grafos para análise estrutural;
- ferramentas de armazenamento colunar para tabelas grandes;
- frameworks de simulação neuronal apenas após comparar dependências e adequação;
- pytest para testes;
- ferramentas de profiling para desempenho.

Não selecionar automaticamente um framework de simulação antigo ou com dependências difíceis apenas por semelhança conceitual. Fazer um pequeno benchmark e avaliar suporte ao sistema operacional, Python, GPU, licença, manutenção e formatos de entrada. A primeira implementação deve permanecer simples e inspecionável.

## 12. Reprodutibilidade de experimentos

Cada experimento deve conter:
- identificador e pergunta;
- hipótese;
- commit SHA ou referência do código;
- versão do Python e dependências;
- dataset/snapshot e hashes;
- configuração completa;
- sementes aleatórias;
- comandos de execução;
- duração e hardware relevante;
- métricas e resultados;
- arquivos de saída;
- comparação com baseline;
- limitações;
- conclusão com categoria de evidência.

Os resultados não devem depender de parâmetros implícitos ou do estado oculto de uma sessão interativa.

## 13. Segurança e integridade

- O simulador deve ser offline por padrão.
- A importação de dados não deve executar arquivos obtidos de terceiros.
- Nunca executar código contido em datasets.
- Validar caminhos, formatos, tamanhos e limites de memória.
- Não incluir tokens, chaves ou segredos em commits, logs ou relatórios.
- Não adicionar execução arbitrária de comandos ou acesso ao sistema operacional como requisito do núcleo neural.
- Qualquer ambiente de tarefas com execução de código deve ser isolado, limitado e testado antes de ser conectado ao projeto.
- Antes de mudanças estruturais, inspecionar o estado do repositório e manter alterações pequenas e reversíveis.

## 14. Riscos e mitigação

### Risco: confundir connectoma com cérebro funcional
**Mitigação:** documentar quais dados são anatômicos e quais parâmetros foram inferidos; testar dinâmica separadamente.

### Risco: escala computacional excessiva
**Mitigação:** começar com subgrafos; perfilar; estimar memória e tempo antes de aumentar.

### Risco: falta de parâmetros biológicos
**Mitigação:** usar parâmetros explícitos e rotulados como hipótese; executar análise de sensibilidade; evitar alegações de fidelidade não verificadas.

### Risco: falta de aprendizagem útil
**Mitigação:** tarefas pequenas, baselines, ablações e critérios de saída claros; aceitar resultados negativos.

### Risco: overfitting ou resultados ocasionais
**Mitigação:** treino/teste separado, múltiplas sementes, avaliação independente e registo de configurações.

### Risco: dependências difíceis de instalar
**Mitigação:** ambiente limpo, conjunto mínimo de dependências e avaliação prévia de compatibilidade.

### Risco: dados grandes no Git
**Mitigação:** manifestos, scripts de download, fixtures pequenos, regras de ignorar verificadas e armazenamento externo apropriado.

### Risco: documentação ficar desatualizada
**Mitigação:** atualizar CONTINUIDADE.md a cada alteração relevante e rever roadmap e plano ao concluir ou alterar uma fase.

### Risco: capacidades externas atribuídas ao núcleo
**Mitigação:** interfaces modulares, controles desligados/ligados, relatórios separados e declaração explícita de uso de módulos externos.

## 15. Processo obrigatório para cada alteração

1. Ler docs/CONTINUIDADE.md e a documentação relacionada.
2. Verificar branch, estado do Git e arquivos alterados.
3. Formular uma tarefa pequena com critério de aceitação.
4. Inspecionar os arquivos antes de editar.
5. Implementar sem remover conteúdo preexistente desnecessariamente.
6. Executar os testes pertinentes e registrar os comandos reais.
7. Inspecionar o diff e confirmar que não foram incluídos dados ou segredos indevidos.
8. Atualizar docs/CONTINUIDADE.md: estado, mudanças, testes, evidências, limitações e próximo passo.
9. Atualizar roadmap e planejamento se a sequência ou as decisões mudaram.
10. Registrar commit SHA quando houver commit; não inventar SHA ou alegar teste que não foi executado.

## 16. Política para trabalho em novos chats

O novo chat deve começar lendo, nesta ordem:
1. README.md;
2. docs/CONTINUIDADE.md;
3. docs/ROADMAP.md;
4. docs/PLANEJAMENTO_DO_PROJETO.md;
5. documentos científicos e de arquitetura citados pela continuidade.

O novo chat deve resumir o estado confirmado e executar somente o próximo passo indicado. Não deve supor que uma fase está concluída, que o dataset foi baixado, que o código foi executado ou que testes passaram sem evidência registrada.

Se a continuidade estiver desatualizada, o novo chat deve primeiro inspecionar o repositório e reconciliar a documentação com o estado real antes de modificar código.

## 17. Critério de sucesso de longo prazo

O sucesso não será definido por ter muitos arquivos, neurônios simulados ou uma demonstração convincente. Será definido por um conjunto crescente de experimentos reproduzíveis que mostrem, com limites claros, quais tarefas o sistema resolve, como aprende, quanto generaliza, quais componentes são necessários e qual é o custo computacional. A hipótese de que o núcleo possa contribuir para tarefas mais complexas será mantida aberta até que evidências comparativas a sustentem.
