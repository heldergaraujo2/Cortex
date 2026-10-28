# CONTINUIDADE DO PROJETO CORTEX

> Documento prioritário para retomar o projeto em um novo chat. Leia este arquivo primeiro, depois README.md, docs/ROADMAP.md e docs/PLANEJAMENTO_DO_PROJETO.md. Não presuma que trabalho não listado aqui foi realizado.

**Última atualização:** 2026-10-28  
**Versão:** 1.1 — arquitetura coletiva aprovada como hipótese  
**Estado geral:** Fase 0 — documentação fundacional criada; auditoria técnica e implementação ainda não realizadas.  
**Repositório:** https://github.com/heldergaraujo2/Cortex  
**Clone informado:** https://github.com/heldergaraujo2/Cortex.git  
**Próximo passo:** Fase 1 — auditar repositório e ambiente real, sem apagar ou sobrescrever nada.

---

## 1. Instruções obrigatórias para novos chats

1. Leia este arquivo integralmente antes de propor ou executar alterações.
2. Leia README.md, docs/ROADMAP.md e docs/PLANEJAMENTO_DO_PROJETO.md.
3. Inspecione o estado atual do GitHub e, quando o trabalho ocorrer no PC, o estado real do clone local. Não confunda o estado remoto com o estado local.
4. Não assuma que código foi executado, testes passaram ou dados foram baixados sem evidência registrada aqui.
5. Execute apenas o próximo passo verificável indicado na seção 8, salvo nova instrução explícita do responsável.
6. Antes de editar, verifique arquivos existentes, branch, alterações locais, arquivos não rastreados e dados locais. Não use comandos destrutivos como reset/clean ou exclusões em massa.
7. Após qualquer alteração relevante em código, dados, dependências, testes, arquitetura, plano ou resultados, atualize este arquivo no mesmo conjunto lógico de mudanças.
8. Registre somente resultados reais. Não invente comandos, resultados de testes, hashes, números de dataset, commits ou conclusões.
9. Classifique afirmações relevantes como CONFIRMADO, FORTEMENTE INDICADO, HIPÓTESE ou DESCONHECIDO.
10. Se houver divergência entre este arquivo e o repositório, inspecione o estado real, preserve alterações existentes e documente a resolução.
11. Não misture Cortex com Lúmen ou outros repositórios. Integrações futuras exigem decisão explícita.
12. Ao encerrar uma sessão, deixe um único próximo passo prioritário, com pré-requisitos e critérios de aceitação.

## 2. Intenção e direção do projeto

Cortex pretende construir uma IA experimental cujo núcleo computacional seja inspirado no connectoma real da mosca-da-fruta (*Drosophila melanogaster*). A intenção é investigar se um grafo neural anatomicamente informado, equipado com dinâmica neuronal, transmissão sináptica, entradas, aprendizagem, memória e tarefas controladas, consegue aprender comportamentos observáveis e úteis.

A direção de longo prazo contempla aprendizagem e resolução de tarefas concretas, com interesse futuro em programação e codificação. Isso é uma meta de investigação, não uma capacidade já demonstrada.

### Limites que devem permanecer explícitos
- O connectoma é um mapa de ligações; não é, por si só, um cérebro funcional pronto para executar.
- A anatomia disponível não determina todos os pesos, atrasos, dinâmicas, estados ou regras de aprendizagem.
- Não alegar consciência, senciência, inteligência geral ou reconstrução funcional completa sem evidência específica.
- Não tentar simular o dataset inteiro antes de validar circuitos pequenos e medir recursos.
- O núcleo neural inicial deve ser avaliado sem depender de um LLM convencional, para que sua aprendizagem possa ser medida isoladamente.
- Módulos externos de IA, ferramentas convencionais ou LLMs poderão ser avaliados no futuro, mas separados do núcleo, opcionais e comparados por ablação.
- Estudos do cérebro humano ou de outros animais podem informar hipóteses, mas não transformam Cortex em uma cópia do cérebro humano.
- A meta de codificação é futura e precisa ser testada; não presumir que circuitos da mosca são diretamente adequados a tarefas abstratas.

## 3. Estado atual verificado

### 3.1 Repositório remoto
**CONFIRMADO:** o responsável forneceu https://github.com/heldergaraujo2/Cortex.git.

**CONFIRMADO:** na primeira tentativa de leitura de README via integração GitHub, a API informou que o repositório estava vazio. Isso descreve o estado observado naquele momento, antes dos primeiros arquivos serem criados.

**CONFIRMADO:** foram criados no repositório:
- README.md — visão geral, princípios, fontes e estado inicial.
- docs/ROADMAP.md — fases, objetivos, entregáveis e critérios de saída.
- docs/PLANEJAMENTO_DO_PROJETO.md — plano técnico/científico, arquitetura, avaliação, riscos e processo de mudança.
- docs/CONTINUIDADE.md — este arquivo.

**DESCONHECIDO:** se o responsável já clonou o repositório no PC, qual é o caminho local, qual branch local está ativa e se há alterações locais.

**DESCONHECIDO:** sistema operacional, versões de Python/Git, RAM, GPU/VRAM, espaço em disco e demais capacidades do ambiente que será usado para executar Cortex. Não reutilizar automaticamente informações de hardware de outros projetos.

### 3.2 Commits documentais confirmados
1. README.md — commit SHA 5f271baf5a025a76959693ef934cb5a0b4f20522.
2. docs/ROADMAP.md — commit SHA bdcea06ab7538be9995c5e771dd9e1d4f7ccb156.
3. docs/PLANEJAMENTO_DO_PROJETO.md — commit SHA 9918496c60fe0e45cc41852c9b2bf7b38240636c.
4. docs/CONTINUIDADE.md — commit SHA a72670a6dc79fe9e8305cb5da6f92aa7f223d850.

Esses SHAs são referências de alterações documentais no remoto; não afirmam que houve clone, pull, execução local ou teste de código.

### 3.3 Código, dados e testes
- **CONFIRMADO:** nenhum código funcional do simulador foi criado nesta etapa documental.
- **CONFIRMADO:** nenhum dataset do FlyWire foi baixado para este projeto durante esta etapa.
- **CONFIRMADO:** nenhum teste de software ou benchmark do Cortex foi executado.
- **CONFIRMADO:** não existe ainda evidência de dinâmica neuronal, plasticidade, memória funcional, treino ou tarefa aprendida.
- **DESCONHECIDO:** árvore atual do repositório após a criação dos documentos, a ser verificada na Fase 1.
- **DESCONHECIDO:** dependências e compatibilidade do ambiente de desenvolvimento.

## 4. Decisões e princípios estabelecidos

### D-001 — Projeto independente
Cortex é um projeto próprio. Não importar automaticamente arquivos, configurações ou dependências de Lúmen ou de outros projetos.

### D-002 — Núcleo neural sem LLM convencional inicialmente
A primeira avaliação do núcleo deve medir aprendizagem sem delegar capacidade a um modelo de linguagem externo. Um LLM pode ser considerado posteriormente como comparador ou módulo opcional.

### D-003 — Connectoma real como âncora estrutural
Investigar datasets públicos de connectoma, com prioridade inicial para FlyWire/Codex, em vez de inventar uma topologia e chamá-la de cérebro da mosca.

### D-004 — Começar por circuito pequeno
A primeira implementação deve usar um subgrafo pequeno, selecionado com critérios documentados e suficientemente compreendido para ter entradas, saídas e testes mensuráveis.

### D-005 — Separar estrutura, dinâmica e aprendizagem
Importar o grafo, simular atividade e aprender são tarefas distintas. Cada camada deve ter testes e critérios próprios.

### D-006 — Evidência explícita
Usar CONFIRMADO, FORTEMENTE INDICADO, HIPÓTESE e DESCONHECIDO. Distinguir dados biológicos, parâmetros estimados e escolhas de engenharia.

### D-007 — Não escalar antes de medir
Medir memória, tempo e estabilidade em circuitos pequenos antes de aumentar o número de neurônios/sinapses.

### D-008 — Documentação viva
Atualizar este arquivo a cada alteração relevante. Atualizar roadmap e plano quando houver mudança de escopo, sequência, arquitetura, critérios ou decisões.

### D-009 — Dados grandes fora do Git por padrão
Versionar scripts, manifestos, metadados úteis e fixtures pequenos. Evitar dumps, volumes e outros artefatos grandes no Git sem decisão explícita e análise de tamanho e termos.

### D-010 — Mudanças seguras
Inspecionar antes de editar. Não remover dados ou arquivos preexistentes sem autorização e justificativa. Não alegar que testes passaram se não foram executados.

### D-011 — Quatro instâncias completas com especializações experimentais
O Cortex deverá permitir quatro instâncias completas e independentes do connectoma de referência, inicialmente designadas C1 Coordenador, C2 Percepção, C3 Aprendizagem e C4 Ação. Os papéis são hipóteses de engenharia e devem ser ajustados à luz do dataset/circuitos escolhidos. Esta arquitetura ainda não foi implementada.

### D-012 — Cérebro coordenador com orquestração de segurança
C1 coordena tarefas e consolida resultados, mas não é a única fonte de verdade. Um orquestrador convencional cuida de contratos, timeouts, registos e recuperação; não é contado como um quinto cérebro. A utilidade do coordenador precisa de ser comparada com cooperação sem coordenador e com agregação simples.

### D-013 — Memória coletiva partilhada
As quatro instâncias consultam uma memória explícita comum com proveniência, versionamento e resolução de conflitos. Estado neural dinâmico e parâmetros plásticos permanecem independentes inicialmente. Partilha de experiências/informações é distinta de fundir os estados neurais. O benefício da memória partilhada será medido por ablações.

### D-014 — Escala para quatro apenas depois de benchmarks
Não executar quatro instâncias completas antes de validar um circuito mínimo e medir o custo no hardware real. A sequência obrigatória continua a ser auditoria, seleção de dataset/circuito, protótipo, profiling e só depois escalada.

## 5. Fontes científicas iniciais verificadas

### Fonte primária de dados: FlyWire Codex
- Página: https://codex.flywire.ai/
- FAQ: https://codex.flywire.ai/faq

**CONFIRMADO a partir das páginas públicas consultadas em 2026-10-28:** o Codex descreve vários datasets de connectoma e oferece downloads estáticos para datasets FlyWire, incluindo FAFB e BANC. A FAQ recomenda arquivos estáticos para análise em lote e diferencia snapshots consolidados de consultas live.

**CONFIRMADO:** a página pública consultada apresentava para FAFB v783 139.255 neurônios e 3.732.460 conexões; para BANC v888, 158.262 neurônios e 3.037.361 conexões. Esses números descrevem contagens de conexões do grafo apresentadas no Codex, não a contagem de sinapses individuais. Reconfirmar valores e definições ao escolher o dataset.

### Artigo científico
- Dorkenwald et al., “Neuronal wiring diagram of an adult brain”, Nature (2024): https://www.nature.com/articles/s41586-024-07558-y

O artigo indica disponibilidade pública dos dados, acesso por Codex e ferramentas programáticas como CAVE/cloudvolume, além de tutoriais.

### Tutoriais e dados
- FlyConnectome: https://github.com/seung-lab/FlyConnectome
- Dados de conectividade no Zenodo: https://doi.org/10.5281/zenodo.10676866

### Cuidado de interpretação
Um conjunto de 139 mil neurônios não significa que o sistema já tenha dinâmica funcional ou comportamento aprendido. Contagem de neurônios, número de pares conectados e número de sinapses são medidas distintas. Todo dataset selecionado precisa de versão, esquema, limiares e fonte registrados.

## 6. Roadmap resumido e estado de cada fase

| Fase | Tema | Estado observado | Critério principal |
|---|---|---|---|
| 0 | Fundação documental | Documentos iniciais criados | Documentação completa e alinhada |
| 1 | Auditoria do repositório e ambiente | Não iniciada | Estado local/remoto e ambiente documentados |
| 2 | Revisão científica e seleção do dataset | Pesquisa inicial feita; decisão não tomada | Dataset/snapshot e circuito inicial justificados |
| 3 | Importação e integridade de dados | Não iniciada | Pipeline reproduzível e testes de integridade |
| 4 | Grafo e análise estrutural | Não iniciada | Grafo dirigido e métricas verificadas |
| 5 | Primeiro circuito real | Não iniciado | Subgrafo pequeno, anotado e com I/O mensurável |
| 6 | Dinâmica neuronal e sináptica | Não iniciada | Equações, unidades e testes numéricos |
| 7 | Simulador e baseline | Não iniciado | Execução reproduzível e baseline mensurável |
| 8 | Plasticidade e aprendizagem | Não iniciada | Melhoria testada contra controle sem aprendizagem |
| 9 | Memória e tarefas sequenciais | Não iniciada | Persistência e retenção testadas |
| 10 | Integração modular | Não iniciada | Contratos e ablações por módulo |
| 11 | Escala e otimização | Não iniciada | Custo medido e otimizações verificadas |
| 12 | Avaliação e replicação | Não iniciada | Resultados principais reproduzíveis |
| 13 | Ferramentas e interface | Não iniciada | Fluxos experimentais utilizáveis |
| 14 | Release experimental | Não iniciada | Instalação e demonstração reproduzíveis |

Consultar docs/ROADMAP.md para os detalhes de cada fase e seus entregáveis.

## 7. Registro de alterações desta sessão

### Alteração 1.0 — Decisão da arquitetura híbrida coletiva (2026-10-28)
- **Objetivo:** converter as preferências do responsável em decisões arquiteturais documentadas.
- **Motivação/hipótese:** investigar se quatro instâncias completas, especializadas e cooperantes, com memória partilhada e um coordenador, melhoram tarefas comparadas com uma instância isolada.
- **Arquivos alterados:** README.md; docs/ROADMAP.md; docs/PLANEJAMENTO_DO_PROJETO.md; docs/CONTINUIDADE.md; docs/ARCHITECTURE.md.
- **Fontes e dados usados:** decisões de arquitetura fornecidas na conversa; nenhuma nova fonte científica ou dataset foi consultado nesta alteração.
- **Comandos executados:** nenhum comando local; alterações documentais realizadas diretamente no GitHub.
- **Testes executados:** nenhum teste de software; o projeto continua sem código funcional.
- **Resultados reais:** documento de arquitetura criado; papéis C1–C4, memória coletiva versionada, riscos do coordenador, critérios de ablação e sequência incremental registados. Ainda não existe implementação nem benchmark.
- **Falhas e limitações:** papéis não validados biologicamente; custo de execução desconhecido; memória coletiva e coordenação ainda não implementadas.
- **Classificação da evidência:** CONFIRMADO para a decisão documental; HIPÓTESE para benefícios de especialização, coordenação e memória partilhada.
- **Commit/branch/SHA (branch main):** docs/ARCHITECTURE.md commit `ca7d70c81c38c60317c784916497d4b9c51d2382`; README.md commit `6187ce00a6b022f43543a493ff781c651914d576`; docs/ROADMAP.md commit `26eb8841623b544706e66b3ccc60a3a7f898e985`; docs/PLANEJAMENTO_DO_PROJETO.md commit `4c1e2bf37ee196cd582bf1f2d09602f5e2332fe3`; docs/CONTINUIDADE.md primeira atualização desta decisão `c71f3b7e40d5496413fd99de59036986d6a28f86`. Este registro final de SHA será atualizado pelo próprio commit desta alteração.
- **Impacto no roadmap:** fases 9–11 precisarão contemplar memória coletiva, múltiplas instâncias, coordenação e ablações; Fase 1 continua prioritária.
- **Decisões tomadas ou alteradas:** quatro cérebros em vez de cinco; um dos quatro assume coordenação; memória explícita coletiva; estados neurais e parâmetros plásticos separados inicialmente.
- **Próximo passo único:** executar a auditoria da Fase 1 do repositório e do ambiente real.
- **Critério de aceitação do próximo passo:** caminho/estado do clone, branch, commit, arquivos locais, sistema, Python/Git, RAM, GPU/VRAM e espaço em disco documentados sem apagar ou sobrescrever dados.

## 7.1 Registro de alterações anterior

### Alteração 0.1 — Inicialização documental (2026-10-28)
**Objetivo:** estabelecer a intenção, roadmap, planejamento e mecanismo de continuidade antes de criar código ou importar dados.

**Arquivos criados:**
- README.md
- docs/ROADMAP.md
- docs/PLANEJAMENTO_DO_PROJETO.md
- docs/CONTINUIDADE.md

**Resultado confirmado:**
- README, roadmap e planejamento foram criados por commits remotos identificados na seção 3.2.
- Este arquivo foi preparado para registrar o estado inicial.
- O roadmap divide o trabalho em 15 fases (0 a 14), com objetivos, atividades, entregáveis e critérios de saída.
- O planejamento define método científico, arquitetura modular proposta, avaliação, riscos e processo de mudança.

**Testes:** nenhum teste de software foi executado; ainda não existe código funcional a testar.

**Limitações:** não foi feita auditoria local; não foi selecionado um dataset final; não foram baixados dados; não foram instaladas dependências; não foi implementado simulador.

**Evidência:** CONFIRMADO para criação documental remota; DESCONHECIDO para estado do PC e execução local.

**Próximo passo:** Fase 1 — auditar repositório e ambiente.

## 8. Próxima tarefa prioritária: Fase 1 — auditoria

### Objetivo
Estabelecer um retrato confiável do estado real antes de criar a estrutura de código.

### Sequência recomendada
1. Verificar no GitHub os arquivos e o commit atual.
2. Confirmar o caminho do clone local ou orientar a clonagem apenas se ainda não existir.
3. No clone, inspecionar branch, commit atual, status, arquivos rastreados e não rastreados. Não descartar mudanças locais.
4. Verificar versão do sistema operacional, Python, Git, RAM, GPU/VRAM e espaço disponível, sem expor informação pessoal desnecessária.
5. Conferir se existem arquivos locais que não aparecem no estado remoto e preservá-los.
6. Escolher versão de Python e estratégia de ambiente somente depois de confirmar compatibilidade.
7. Criar um relatório da auditoria, registrando comandos e saídas relevantes.
8. Atualizar este arquivo com o estado observado e o próximo passo.

### Critérios de aceitação
- Caminho e estado do clone local conhecidos, se houver.
- Branch e commit registrados.
- Arquivos locais não commitados e não rastreados identificados.
- Ambiente e recursos documentados.
- Nenhum arquivo foi apagado ou sobrescrito.
- Próximo passo baseado em evidências.

### Não fazer nesta fase
- Não baixar o connectoma inteiro.
- Não instalar frameworks pesados de simulação antes de definir a necessidade.
- Não implementar aprendizagem antes de ter circuito e tarefa definidos.
- Não mover ou renomear arquivos existentes sem inventário.
- Não presumir que o ambiente de outro projeto é o ambiente do Cortex.

## 9. Formato obrigatório para atualizações futuras

A cada alteração relevante, acrescentar uma entrada cronológica nesta estrutura:

### Alteração X.Y — Título (AAAA-MM-DD)
- **Objetivo:**
- **Motivação/hipótese:**
- **Arquivos alterados:**
- **Fontes e dados usados:**
- **Comandos executados:**
- **Testes executados:**
- **Resultados reais:**
- **Falhas e limitações:**
- **Classificação da evidência:**
- **Commit/branch/SHA:**
- **Impacto no roadmap:**
- **Decisões tomadas ou alteradas:**
- **Próximo passo único:**
- **Critério de aceitação do próximo passo:**

Não preencher campos com suposições. Se algo não foi verificado, escrever “não verificado” ou “não executado”.

## 10. Checklist de encerramento de toda sessão

- [ ] Inspecionar o diff final.
- [ ] Confirmar que nenhum segredo ou dataset indevido foi adicionado.
- [ ] Executar testes relevantes e registrar o resultado exato; se não foram executados, dizer isso.
- [ ] Atualizar este arquivo.
- [ ] Atualizar roadmap/plano se houver mudança de fase, arquitetura, critérios ou prioridades.
- [ ] Registrar branch e commit SHA real, se existir.
- [ ] Listar falhas e questões em aberto.
- [ ] Definir apenas um próximo passo prioritário.
- [ ] Garantir que um novo chat consiga retomar sem depender de mensagens antigas.

## 11. Questões em aberto

1. Qual é o caminho local do clone e qual é o estado atual do PC?
2. Qual dataset/snapshot será escolhido após a revisão detalhada?
3. Qual circuito pequeno oferece melhor combinação de relevância científica, documentação e viabilidade?
4. Qual modelo neuronal inicial permite simulação testável com o ambiente disponível?
5. Quais parâmetros são fornecidos pelo dataset e quais precisarão ser estimados?
6. Qual tarefa inicial permite distinguir aprendizagem real de comportamento fixo ou acaso?
7. Quais metas de desempenho são realistas no hardware medido?
8. Como serão armazenados datasets, checkpoints e resultados grandes sem tornar o Git impraticável?

Estas questões não bloqueiam a auditoria inicial; devem ser resolvidas na fase apropriada.

## 12. Resumo de retomada em poucas linhas

Cortex está na etapa de fundação documental. O repositório estava vazio na primeira inspeção e recebeu README, roadmap, planejamento e continuidade. A missão é investigar um núcleo neural inspirado em connectoma real de mosca, começando pequeno, separando estrutura/dinâmica/aprendizagem, medindo resultados e sem usar um LLM convencional como núcleo inicial. Nenhum código funcional foi implementado, nenhum dataset foi baixado e nenhum teste foi executado. O próximo passo é auditar o estado real do repositório e do ambiente, preservar qualquer alteração local e só então iniciar a seleção técnica do dataset e do circuito.
