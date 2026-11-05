# CONTINUIDADE DO PROJETO CORTEX

> Documento prioritário para retomar o projeto em um novo chat. Leia este arquivo primeiro, depois README.md, docs/ROADMAP.md e docs/PLANEJAMENTO_DO_PROJETO.md. Não presuma que trabalho não listado aqui foi realizado.

**Última atualização:** 2026-11-05  
**Versão:** 2.6 — perfis estruturais reais por alvo T4 concluídos  
**Estado geral:** auditoria, importação e anotação T4 concluídas (#82, #99, #110); perfis por alvo/coluna executados com sucesso no FAFB #128. Das 6.236 células T4 com inputs candidatos, 5.981 têm coluna/hemisfério atribuído e 255 não; 51.387 linhas de aresta estão ligadas a alvos atribuídos, 1.897 não; zero divergências de hemisfério. Cortex CI #165 passou com 95 testes em Python 3.11–3.13. O modelo assinado continua sintético; faltam posições/colunas dos candidatos pré-sinápticos e evidência fisiológica por aresta.  
**Repositório:** https://github.com/heldergaraujo2/Cortex  
**Branch de trabalho:** `data/fafb-v783-inputs` — PR #1 permanece aberto e não integrado em `main`.  
**Política de execução:** GitHub-first; testes e experimentos remotos primeiro. PC reservado para profiling, validação Windows ou quando houver necessidade concreta.  
**Próximo passo único:** inspecionar a CI acionada pela auditoria T4, corrigir falhas e examinar `fafb_v783_t4_input_audit.json` antes de definir quais mecanismos podem ser modelados.

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
- **CONFIRMADO:** desde a atualização de 2026-10-28, existe um scaffold Python e contratos de mensagens; nenhum código funcional de simulador neural foi criado.
- **CONFIRMADO:** nenhum dataset do FlyWire foi baixado para este projeto durante esta etapa.
- **CONFIRMADO:** 11 testes passaram em ambiente isolado Python 3.13 com os ficheiros recuperados do GitHub; a instalação editável do pacote também passou. Workflow GitHub Actions configurado para Python 3.11, 3.12 e 3.13, mas seu resultado não foi verificável pelo conector. Nenhum teste foi executado no PC do responsável.
- **CONFIRMADO:** não existe ainda evidência de dinâmica neuronal, plasticidade, memória funcional, treino ou tarefa aprendida.
- **CONFIRMADO:** a árvore remota inclui documentação, pacote `cortex`, testes, `pyproject.toml`, `.gitignore` e workflow CI. **DESCONHECIDO:** árvore e estado do clone local, caso exista.
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

## 7.20 Fase 7 — auditoria real dos inputs candidatos a T4 concluída (2026-11-05)

- **Execução:** FAFB v783 Data Validation #82, run `41948702974`, sucesso. Artefato `fafb-v783-validation-report`, ID `13380560010`; contém `fafb_v783_t4_input_audit.json`. SHA-256 do ZIP: `a947761f29a87e101f2b18d901a8691bc4796aa3e3cdd47dde69ad8d2fef08c7`.
- **CI:** Cortex CI #122, run `41948813842`, sucesso; 65 testes passaram em cada matriz Python 3.11, 3.12 e 3.13. Log da matriz 3.11 confirma `65 passed`.
- **Dados:** 5.342.446 linhas de conexões; 5.318.409 linhas com ambos os IDs mapeados; 53.284 linhas de conexão de Mi1/Tm3/Mi4/Mi9/C3/TmY15/CT1 para T4a–T4d, considerando todos os neuropilos.
- **Tipos primários:** Mi1 1.581; Tm3 1.756; Mi4 1.532; Mi9 1.551; C3 1.535; TmY15 257; CT1 2; T4a 1.457; T4b 1.507; T4c 1.710; T4d 1.569.
- **Medula:** 25.904 linhas ME_L e 26.656 ME_R (52.560 total); soma estrutural de `syn_count` 574.359 nessas duas regiões, mantendo no relatório a separação por tipo/neuropilo/`nt_type`.
- **Rótulos no arquivo:** ACH 31.333 linhas; GABA 17.098; GLUT 4.853. A distribuição não é perfeitamente uniforme por tipo (por exemplo, Mi9 mistura GLUT e GABA; aparecem algumas exceções nos outros tipos). Codex diferencia `nt_type` previsto de `nt_type_verified` curado; os rótulos não são tratados como sinal funcional confirmado.
- **Observação:** CT1 tem dois IDs primários, mas milhares de linhas de conexão para T4; linhas não equivalem a neurónios.
- **Documento completo:** `docs/FASE_7_AUDITORIA_INPUTS_T4.md`.
- **Conclusão:** CONFIRMADO para presença de classes e conexões estruturais no snapshot. FORTEMENTE INDICADO pela literatura para papéis transmissores gerais de várias classes. DESCONHECIDO para sinal fisiológico por aresta, eficácia, atraso e contribuição causal específica. Nenhuma DSI foi calculada nesta auditoria.
- **Próxima subetapa:** construir um módulo experimental T4 assinado e separado do baseline v0. Distinguir neurotransmissor, efeito pós-sináptico e polaridade da resposta pré-sináptica (especialmente Mi9); parâmetros de atraso serão varridos como hipóteses de engenharia, não tratados como tempos biológicos medidos.
- **Branch:** `data/fafb-v783-inputs`; PR #1 permanece aberto e `main` não foi alterada.

## 7.21 Fase 7 — protótipo sintético T4 com entradas assinadas (2026-11-05)

- **Implementação:** `cortex/t4_mechanism.py` separa sinal pós-sináptico, polaridade da resposta pré-sináptica, offset espacial, constante temporal, atraso e ganho.
- **Braços exploratórios:** Mi1/Tm3 ACH (+); Mi4/C3/CT1/TmY15 GABA (-); Mi9 GLUT com resposta OFF e efeito inibitório pós-sináptico, representado como desinibição em estímulo ON.
- **Salvaguarda:** posições, ganhos, tau e atrasos são parâmetros de engenharia não calibrados; não são extraídos de FAFB. O módulo não consome ainda IDs/arestas reais nem mapeamento de campo visual.
- **Demonstração:** `scripts/run_t4_mechanism_demo.py` compara varreduras sintéticas opostas com o mesmo número de eventos. Saídas CI: integral forward 2,107407; reverse 1,301926; assimetria sintética 0,236258. O resultado não é DSI biológico nem identifica PD/ND.
- **Controlos:** sem estímulo resulta em zero; braço direto isolado e simétrico não gera assimetria; entrada GABA reduz a resposta do braço direto; Mi9 com polaridade OFF e sinapse inibitória gera drive líquido positivo (desinibição) no modelo.
- **CI #129:** 73 testes passaram em Python 3.11, 3.12 e 3.13.
- **CI #130:** 73 testes passaram nas três versões e o CLI foi executado em todas, reproduzindo os mesmos valores da demonstração.
- **Documento:** `docs/FASE_7_MODELO_T4_ASSINADO.md`.
- **Conclusão:** protótipo computacional sintético validado; mecanismo biológico, parâmetros fisiológicos, posições de inputs e seletividade direcional real continuam não demonstrados.

## 7.22 Fase 7 — importação estrutural das arestas reais T4 (2026-11-05)

- **Implementação:** `cortex/t4_inputs.py`, `tests/test_t4_inputs.py` e `scripts/import_t4_input_edges.py`.
- **Preservação:** importa linhas dirigidas de Mi1/Tm3/Mi4/Mi9/C3/TmY15/CT1 para T4a–T4d, preservando IDs, neuropilo, `syn_count` e `nt_type`; não deduplica nem atribui sinal.
- **Execução real:** FAFB Data Validation #99, run `41949691726`, sucesso; artefato ID `13381150256`, contendo `fafb_v783_t4_input_edges.json`.
- **Resultado:** 53.284 linhas; 7.028 IDs pré-sinápticos distintos; 6.236 IDs T4 pós-sinápticos; 143 grupos. Linhas por neuropilo: ME_L 25.904; ME_R 26.656; LOP_L 245; LOP_R 368; LO_L 60; LO_R 47; AME_L 3; UNASGD 1.
- **CI:** #135 e #137 passaram com 81 testes em Python 3.11, 3.12 e 3.13. #137 executou também o demo sintético T4 em todas as versões.
- **Limite crítico:** o CSV consolidado de tipos contém somente `root_id`, `primary_type`, `additional_type(s)`; o CSV de conexões contém `nt_type`, não `nt_type_verified`. A documentação Codex diferencia previsão e verificação curada. Não existe base no snapshot atual para assinar cada aresta como fisiologicamente excitatória/inibitória.
- **Conclusão:** importação estrutural real confirmada; sinal por aresta, eficácia, atrasos e geometria funcional continuam não resolvidos.
- **Próxima subetapa:** obter uma fonte de neurotransmissores verificados e mapear espacialmente os candidatos pré-sinápticos; depois criar perfis estruturais por alvo T4 e integrar ao modelo sem alterar baseline v0.

## 7.23 Fase 7 — previsões de neurotransmissor por neurónio (2026-11-05)

- **Fonte:** produto público Codex FAFB v783 `neurons.csv.gz`, descarregado durante o workflow, não versionado no repositório. SHA-256: `6a6b3759e635f0f35a677d169052362131ec61d95f55919298b55c43fce4e719`.
- **Implementação:** `cortex/t4_annotations.py`, `tests/test_t4_annotations.py`, `scripts/audit_t4_neuron_annotations.py`.
- **Execução:** FAFB Data Validation #110, run `41951036288`, sucesso; artefato ID `13381600336`.
- **CI:** Cortex CI #155, run `41951567048`, 88 testes aprovados em Python 3.11–3.13; demo sintético executado em todas as versões.
- **Cobertura:** 7.028/7.028 IDs pré-sinápticos mapeados; 53.284/53.284 linhas de aresta associadas a um registo de neurónio.
- **Rótulos:** 50.630 linhas com previsão não vazia; 2.654 linhas com previsão vazia; 0 divergências entre previsão não vazia do neurónio e `nt_type` da linha de conexão.
- **Confiança:** score mediano por classe: C3 0,78; CT1 0,66; Mi1 0,63; Mi4 0,87; Mi9 0,58; Tm3 0,70; TmY15 0,81.
- **Mi9:** 3.700 linhas GLUT, 544 GABA, 2 ACH e 1.434 sem rótulo; baixa confiança relativa e mistura exigem análise por neurónio.
- **Limite:** concordância entre os dois campos Codex é consistência interna, não validação independente. O produto tem `nt_type` previsto e `nt_type_score`, mas não `nt_type_verified`. Nenhum sinal fisiológico por aresta foi atribuído.
- **Próxima subetapa:** construir perfis por T4-alvo e subtipo; juntar os alvos T4 à coluna existente e investigar uma fonte espacial validada para os candidatos pré-sinápticos adicionais.

## 7.24 Fase 7 — perfis estruturais por alvo T4 e coluna (2026-11-05)

- **Implementação:** `cortex/t4_profiles.py`, `tests/test_t4_profiles.py`, `scripts/summarize_t4_target_profiles.py`.
- **Execução real:** FAFB Data Validation #128, run `41951942609`, sucesso; artefato ID `13381252165`; relatório `fafb_v783_t4_target_profiles.json`.
- **Junção:** 53.284 arestas candidatas para 6.236 alvos T4 distintos; junção exata por `post_root_id` com `column_assignment.csv.gz`.
- **Cobertura:** 5.981 alvos atribuídos, 255 não atribuídos; 51.387 linhas de aresta com alvo atribuído, 1.897 sem.
- **Por subtipo:** T4a 1.440/1.456 (98,901%); T4b 1.492/1.506 (99,070%); T4c 1.551/1.705 (90,968%); T4d 1.498/1.569 (95,475%).
- **Consistência:** zero divergências entre o sufixo de lado do neuropilo e o hemisfério da atribuição do T4-alvo.
- **Estrutura:** 221 grupos agregados e 6.236 perfis individuais. `syn_count` permanece contagem estrutural, não eficácia.
- **CI #165:** 95 testes aprovados em Python 3.11, 3.12 e 3.13.
- **Limite:** a atribuição resolve o alvo T4, não os candidatos pré-sinápticos Mi4/Mi9/C3/CT1/TmY15. Não calcular offsets/direção com base apenas na posição do alvo.
- **Próxima subetapa:** investigar mapeamento espacial validado dos 7.028 IDs pré-sinápticos, construir perfis por coluna e procurar evidência independente de receptores/sinal.

## 8. Estratégia de execução atual — GitHub-first

O responsável decidiu adiar o primeiro teste local no Windows e continuar o desenvolvimento no GitHub. Esta decisão é compatível com as tarefas atuais: a CI executa testes automatizados e os workflows podem processar os arquivos FAFB já presentes na branch.

### Regras
1. Executar testes unitários e experimentos com dados reais no GitHub Actions sempre que o workflow suportar a tarefa.
2. Inspecionar logs e artefatos reais antes de marcar uma fase como concluída.
3. Não afirmar compatibilidade Windows, desempenho local ou uso de GPU sem teste no PC.
4. Preservar a branch `data/fafb-v783-inputs` e o PR #1; não integrar em `main` sem decisão explícita.
5. Fazer o primeiro teste local quando houver profiling, necessidade de bibliotecas específicas, limite de runner, validação Windows ou uma comparação de desempenho que não possa ser feita remotamente.

### Próximo gate remoto
- Investigar uma transformação espacial validada para os 7.028 IDs pré-sinápticos candidatos; a coluna atual cobre somente L1, Mi1, Tm3 e T4.
- Usar coordenadas/morfologia apenas após validar semântica e desempenho em tipos com atribuição conhecida; não inferir p/q de coordenadas brutas.
- Construir perfis estruturais por coluna e subtipo a partir dos 6.236 perfis T4 existentes, mantendo neuropilo, rótulo, score e syn_count separados.
- Procurar evidência independente/curada de receptores e neurotransmissores; o dump v783 não contém `nt_type_verified`.
- Integrar sinais somente quando sustentados; manter desconhecidos os casos vazios/ambíguos.
- Executar ablações/sensibilidade ME_L/ME_R; DSI biológico continua bloqueado até mapear PD/ND.

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

O Cortex já possui o piloto FAFB v783 importado, validação espacial/colunar, baseline estrutural rate-based v0 e diagnóstico de frentes na malha medular p/q. A Fase 6 passou na validação real ME_L/ME_R do GitHub Actions e a suíte CI aprovou 61 testes em Python 3.11, 3.12 e 3.13. A assimetria +/− observada é pequena e não demonstra seletividade direcional biológica; a rede ainda não inclui entradas inibitórias, atrasos fisiológicos ou calibração. O repositório está pronto para o primeiro teste local no PC Windows. Próxima ação: sincronizar a branch `data/fafb-v783-inputs` sem descartar trabalho local e executar `scripts/run_first_pc_validation.ps1`; depois comparar os cinco relatórios locais com o artefato CI #71. O PR #1 continua aberto e `main` não foi alterada.


## 7.2 Registro de alterações 1.2 — bootstrap remoto e revisão de fontes (2026-10-28)

- **Objetivo:** avançar o projeto sem depender do PC, estabelecer base Python testável e comparar fontes científicas para o connectoma.
- **Motivação/hipótese:** um scaffold sem dependências de runtime reduz riscos enquanto o circuito inicial não foi escolhido; BANC pode ser útil para tarefas sensório-motoras por incluir cérebro e cordão nervoso.
- **Arquivos criados:** `pyproject.toml`, `.gitignore`, `cortex/__init__.py`, `cortex/contracts.py`, `cortex/diagnostics.py`, `tests/test_contracts.py`, `tests/test_diagnostics.py`, `.github/workflows/tests.yml`, `docs/CONTRATOS_TECNICOS.md`, `docs/SCIENTIFIC_SOURCES.md`.
- **Arquivos atualizados:** `README.md`, `docs/ROADMAP.md`, `docs/PLANEJAMENTO_DO_PROJETO.md`, este arquivo.
- **Fontes científicas consultadas:** Codex e FAQ oficiais, orientações de licença/citação FlyWire, artigos Nature sobre FAFB e BANC, depósito estático BANC e FlyConnectome.
- **Comandos executados:** nenhum comando local. Alterações e commits realizados via integração GitHub.
- **Testes executados:** nenhum teste executado pelo assistente nesta sessão. Workflow CI configurado para Python 3.11, 3.12 e 3.13; resultado precisa de verificação real antes de declarar sucesso.
- **Resultados reais:** repositório remoto confirmado como público, branch padrão `main`; configuração de pacote e contratos criados; diagnóstico não destrutivo criado; documentação de fonte/dataset e contratos criada.
- **Falhas e limitações:** sem resultado CI verificado até este registo; sem dataset descarregado/inspecionado; sem importador, circuito real, simulador, dinâmica, plasticidade ou memória coletiva funcional; ambiente físico local desconhecido.
- **Classificação da evidência:** CONFIRMADO para os ficheiros/commits remotos e conteúdo dos documentos oficiais consultados; FORTEMENTE INDICADO para BANC v888 como candidato de cobertura sensório-motora; HIPÓTESE para vantagem do BANC no Cortex; DESCONHECIDO para o circuito inicial, desempenho e recursos do PC.
- **Commits remotos desta alteração:** configuração `pyproject.toml` c1556eb7b7b6640dd57e496bb53810ef35e86d2f; `.gitignore` 3358b7403d91d64284a88ebe4bded33d15f7a050; pacote `cortex/__init__.py` 7d4abccecc5d80b36ee5a0a5a8d4da1d7a136665; contratos 9ffaa20092ab9715c1443f04082d7221e803010d; testes de contratos a563305d6c13c658e8de2e25496081925a21d2ef; workflow CI 2313f7b88e39b4eb1704765cad8131ba6da0481d; fontes 95ae02c3506faf902f5901573d680f13648308f0; contratos técnicos d6354de72974d8ba2944dec5f9681aa2b49232b7; diagnóstico a68a39467a2406ecec1ba608dd1c9ad39c5018c3; teste de diagnóstico f8c4b6df89c65f180b407d38c043260d048a39ec3. Commits documentais mais recentes confirmados: README.md `5fbf097ab9fbd76b769861d166baeaab85f3c7e6`; docs/ROADMAP.md `05568dfd3adab9789e85e2bac8c7d2006c2c5afb`; docs/SCIENTIFIC_SOURCES.md `a51fca3d4cd1a980fef752c03b36a16b443113ed`; docs/CONTINUIDADE.md (versão anterior a este ajuste) `dfa906c8887771a6c8e73bd83a2f1d86b77920b2`; docs/CONTRATOS_TECNICOS.md `d6354de72974d8ba2944dec5f9681aa2b49232b7`. A versão atual desta continuidade é o commit que grava este ajuste; consultar o histórico do ficheiro para o SHA exato.
- **Impacto no roadmap:** Fase 1 passa a separar o gate remoto verificável do profiling físico; Fase 2 deve confirmar o dataset e selecionar circuito após inspecionar metadados reais.
- **Decisões tomadas ou alteradas:** estratégia GitHub-first; Python 3.11+; nenhuma dependência de runtime inicial; BANC v888 como candidato principal provisório e FAFB v783 como alternativa/controle; não baixar dados grandes antes de delimitar o circuito.
- **Próximo passo único:** iniciar a Fase 2 com inspeção dos metadados oficiais do FAFB v783 e escolher um circuito pequeno com tarefa observável.
- **Critério de aceitação:** circuito e tarefa têm IDs/limites explícitos, dados necessários identificados, fonte/licença registadas e baseline/medidas definidas antes de importar ou simular.

## 8.1 Execução local segura quando necessária

Quando o projeto exigir validação local, após atualizar o clone sem descartar alterações locais:
1. executar `python -m cortex.diagnostics` no ambiente do Cortex;
2. guardar o relatório fora do Git ou remover dados pessoais/identificadores desnecessários antes de o partilhar;
3. executar `python -m pip install -e ".[dev]"` num ambiente virtual próprio;
4. executar `python -m pytest`;
5. registar versões, resultados e limitações, sem assumir que o CI representa a GPU/RAM do PC.

O diagnóstico apenas lê informação do host e não escreve ficheiros. A instalação deve ser feita explicitamente pelo responsável no ambiente escolhido.


## 7.3 Fecho da Fase 1 — auditoria remota e bootstrap (2026-10-28)

- **Objetivo:** fechar a base remota de engenharia sem depender do PC antes de haver uma necessidade real de profiling.
- **Resultado:** pacote Python mínimo, contratos iniciais, diagnóstico de leitura apenas, configuração de instalação, testes e CI foram criados e verificados no GitHub.
- **Teste executado fora do GitHub Actions:** os ficheiros de código/testes recuperados do GitHub foram executados numa área isolada do ambiente de validação do assistente com Python 3.13. Resultado: `11 passed in 0.10s`. Também foi executada instalação editável com `pip install --no-deps --no-build-isolation -e .` no fixture de validação, que concluiu com `Successfully installed cortex-connectome-0.1.0`.
- **Limite de evidência:** estes resultados não são uma execução no PC do responsável e não confirmam a matriz Python 3.11/3.12/3.13 do GitHub Actions. A consulta de estado de commit devolveu `statuses: []`, e o conector não disponibiliza uma listagem geral das execuções push do workflow. Não declarar o CI remoto como aprovado sem observar uma execução real.
- **Auditoria remota:** repositório público `heldergaraujo2/Cortex`, branch padrão `main`, permissão de escrita confirmada; antes do scaffold não existiam configuração Python, pacote, testes nem workflow CI. Estado local do clone permanece desconhecido.
- **Seleção científica inicial:** FAFB v783 foi escolhido documentalmente para o primeiro protótipo por ser um conectoma do cérebro adulto feminino (inclui lobos ópticos, não inclui cordão nervoso), bem documentado e com licença pública CC BY-NC 4.0 declarada pelo guia oficial FlyWire. BANC v888 fica como possível extensão futura. A seleção do dataset não substitui a seleção do circuito e da tarefa.
- **Critérios cumpridos:** scaffold, contratos, teste unitário, instalação isolada, política de dados e diagnóstico seguro criados; 11 testes passaram no ambiente de validação.
- **Pendências não bloqueantes para iniciar a Fase 2:** confirmar execução GitHub Actions quando possível; estado do PC/clonagem local desconhecido; dados não descarregados; circuito real ainda não escolhido.
- **Decisão de fase:** Fase 1 encerrada para o escopo remoto disponível. O perfil físico do PC fica deliberadamente adiado até que o importador, a simulação ou o profiling o tornem necessário.
- **Próxima fase:** Fase 2 — revisão dos produtos de dados FAFB v783, seleção de circuito real pequeno, definição de tarefa e baseline mensuráveis.


## 7.4 Registo de sessão — seleção do circuito inicial (2026-10-28)

- **Objetivo:** avançar a Fase 2, selecionar um circuito real pequeno por regra reproduzível e definir uma tarefa observável antes de implementar dinâmica neuronal.
- **Fontes consultadas:** FAQ/Codex oficial, portal de downloads e artigos primários sobre conectoma visual e via ON T4. O FAQ oficial indica que o acesso em lote deve usar CSVs estáticos, nomeia `consolidated_cell_types` e `connections_princeton` no exemplo programático, explica os campos de anotação e o limiar padrão FAFB de 5+ sinapses por par. O artigo de Takemura et al. descreve a hipótese de via de movimento baseada em L1, Mi1/Tm3 e T4; a literatura posterior assinala entradas adicionais e incertezas.
- **Decisão:** primeiro núcleo exploratório = `L1 → Mi1/Tm3 → T4`, dataset FAFB v783. O núcleo é parcial e não é alegado como circuito biológico completo.
- **Arquivos criados:** `docs/FASE_2_CIRCUITO_INICIAL.md`, `data/manifests/fafb_v783_t4_on_pilot.json`, `cortex/experiments/__init__.py`, `cortex/experiments/motion_t4.py`, `tests/test_motion_t4_spec.py`.
- **Arquivos atualizados:** `README.md`, `docs/ROADMAP.md`, este arquivo.
- **Validação executada:** os três testes da especificação foram executados num diretório temporário isolado, reproduzindo a especificação e os testes escritos no GitHub; resultado **3 passed in 0.05s**. Isto não valida dados biológicos nem substitui o workflow CI.
- **Dados reais:** nenhum CSV foi descarregado, nenhuma raiz de neurónio (root ID) foi inventada ou registada e nenhum número de neurónios/arestas do subcircuito foi afirmado.
- **Tarefa definida:** estímulo ON sintético com movimento em duas direções, flash estático e ausência de estímulo; métrica candidata = diferença normalizada de resposta T4 entre direções. A aplicabilidade desta métrica está condicionada à validação da correspondência entre posições visuais/colunas e neurónios.
- **Baselines planeadas:** sem seletividade, filtros temporais simples, modelo sem plasticidade, ablação de Mi1/Tm3, direção invertida e flash estático. Nenhuma baseline foi simulada.
- **Limitações:** o núcleo omite entradas conhecidas de T4 (Mi4, Mi9, C3, TmY15, CT1 e potencialmente outras); o conectoma não determina por si só sinais fisiológicos, pesos, atrasos, dinâmica neuronal ou plasticidade.
- **Gate bloqueado:** o portal oficial requer token de conta para obter os recursos. A ferramenta de navegação conseguiu ler a documentação pública, mas não inspecionar metadados autenticados, tamanho/cabeçalhos dos arquivos concretos ou a correspondência espacial. Não pedir nem guardar token em chat ou Git. O gate será resolvido por acesso autorizado aos produtos ou por ficheiros obtidos pelo responsável e partilhados sem credenciais.
- **Estado da Fase 2:** seleção documental do dataset, circuito e desenho experimental concluídos; extração/validação empírica de dados pendente e explicitamente bloqueada por acesso aos produtos. Não declarar a fase de dados completa.
- **Próximo passo único:** obter por via autorizada os metadados e os CSVs mínimos `consolidated_cell_types` e `connections_princeton`, mais uma fonte validada de mapeamento espacial/colunas; registar cabeçalhos, tamanhos, hashes e termos de cada produto antes de construir o importador.


## 7.5 Fecho da Fase 2 — desenho concluído, gate de dados transferido (2026-10-28)

- **Objetivo:** escolher um dataset/snapshot, circuito inicial reproduzível e tarefa mensurável.
- **Decisão de dataset:** FlyWire FAFB v783, com BANC v888 reservado como extensão possível.
- **Decisão de circuito:** núcleo exploratório `L1 → Mi1/Tm3 → T4` da via ON de movimento, com regra de seleção por tipos e pares de arestas. O núcleo é parcial; entradas adicionais de T4 estão documentadas.
- **Decisão experimental:** estímulos sintéticos de movimento em direções opostas, flash estático e ausência de estímulo; métrica candidata baseada na diferença de resposta T4 entre direções, condicionada à existência de um mapeamento espacial validado.
- **Entregáveis:** documento de circuito, manifesto JSON, especificação tipada e três testes; documentação e continuidade atualizadas.
- **Validação:** 3 testes passaram em 0,05s no ambiente temporário isolado. Não houve simulação neural nem leitura de dados biológicos.
- **Fontes:** Codex FAQ/portal, Takemura et al. 2013, Shinomiya et al. 2017, Dorkenwald et al. 2024, depósito Zenodo 10.5281/zenodo.10676866.
- **Cuidado de licença:** as orientações FlyWire para FAFB v783 declaram CC BY-NC 4.0. Depósitos distintos podem ter metadados próprios; verificar os termos do produto exato e não redistribuir se houver conflito não resolvido.
- **Gate transferido para a Fase 3:** a extração empírica requer produtos concretos (mínimo: `consolidated_cell_types`, `connections_princeton`, mais fonte espacial/colunas verificada), cabeçalhos, tamanhos, hashes, licenças e IDs/contagens reais. O portal oficial exige token para obter recursos; nenhum token foi solicitado ou armazenado. Os arquivos ainda não foram baixados.
- **Estado da fase:** Fase 2 encerrada quanto à seleção e ao desenho experimental; gate de dados não está aprovado e não deve ser descrito como concluído.
- **Próximo passo único:** iniciar Fase 3 com aquisição autorizada e validação dos dados mínimos, antes de qualquer importador que os consuma ou simulador.


## 7.6 Início da Fase 3 — revisão do acesso a dados e correção de premissa (2026-10-28)

- **Objetivo:** iniciar a aquisição/validação sem depender do PC antes de esgotar o trabalho possível no repositório e nas fontes públicas.
- **Arquivos inspecionados:** `docs/CONTINUIDADE.md`, `docs/ROADMAP.md`, `docs/SCIENTIFIC_SOURCES.md`, `docs/FASE_2_CIRCUITO_INICIAL.md`, `data/manifests/fafb_v783_t4_on_pilot.json` e `README.md`.
- **Fonte oficial reconsultada:** FAQ Codex https://codex.flywire.ai/faq; guia de licença https://flywire.ai/guidelines; portal https://codex.flywire.ai/api/download?dataset=fafb.
- **Achado documental:** a FAQ atual descreve os produtos estáticos públicos e exemplifica os endpoints `api/download` e `api/download_resource`, usando `consolidated_cell_types` e `connections_princeton`. Ela diz que token CAVE/FlyWire é necessário para operações de permissões do projeto ao vivo, como mapear root IDs e consultar histórico, não afirma que todo download estático exija token.
- **Correção:** a formulação anterior que dizia que o portal de downloads exigia token foi demasiado abrangente e foi corrigida em `docs/FASE_2_CIRCUITO_INICIAL.md`. A autenticação para os produtos estáticos não deve ser presumida; a acessibilidade real precisa ser testada.
- **Tentativa de acesso ao endpoint:** a ferramenta web não conseguiu abrir o endpoint do recurso diretamente; uma tentativa HTTP no ambiente de execução também falhou por indisponibilidade de resolução DNS. Isso é uma limitação do ambiente de validação, não evidência de que o serviço exija token ou esteja indisponível para o utilizador.
- **Dados baixados:** nenhum. Cabeçalhos, tamanhos, linhas, hashes dos arquivos concretos e root IDs continuam **DESCONHECIDOS**. Nenhum segredo foi solicitado ou armazenado.
- **Testes executados:** nenhum teste de software; alteração documental apenas.
- **Classificação da evidência:** **CONFIRMADO** para o texto atual da FAQ e para a alteração remota do documento; **DESCONHECIDO** para a disponibilidade efetiva dos endpoints neste ambiente e para os metadados dos produtos concretos.
- **Commit:** `docs/FASE_2_CIRCUITO_INICIAL.md` atualizado no commit `35c706a0ccfda887697949db179bc57e07ec06a0`. O SHA desta atualização de continuidade será o commit que grava esta entrada.
- **Impacto no roadmap:** Fase 3 continua aberta. O primeiro passo é verificar os metadados públicos e tentar acesso legítimo aos recursos estáticos; só depois decidir se é necessário usar o PC do responsável ou solicitar arquivos obtidos por ele. Acesso ao CAVE ao vivo continua sujeito a autorização própria.
- **Próximo passo único:** inspecionar os metadados e testar o endpoint oficial de download dos produtos FAFB v783 sem credenciais, mantendo o resultado como não verificado se o ambiente continuar sem acesso de rede.
- **Critério de aceitação:** registar nomes/URLs dos produtos, resposta HTTP efetiva, formato, tamanhos e termos aplicáveis; não marcar a aquisição como concluída até ter os arquivos e calcular SHA-256, cabeçalhos e contagens reais.


## 7.7 Alinhamento do roadmap com o gate de acesso (2026-10-28)

- **Objetivo:** garantir que o roadmap não perpetue a premissa demasiado ampla de que todo download Codex exige token.
- **Arquivo atualizado:** `docs/ROADMAP.md`.
- **Alteração:** o aditivo da Fase 2/Fase 3 agora distingue downloads estáticos públicos das operações CAVE/FlyWire ao vivo/protegidas e deixa a acessibilidade real dos endpoints como item por verificar.
- **Fonte:** FAQ oficial do Codex https://codex.flywire.ai/faq, consultada nesta sessão.
- **Testes/comandos:** nenhum teste de software executado; alteração documental remota.
- **Resultado real:** commit do roadmap `7b3b91b70a1786822fa3f7d4c46d9edefab87776`; continuidade anterior sobre acesso corrigido no commit `90ae69c69c9a8850b2391805419923df9783d39a`; correção da frase no documento experimental em `35c706a0ccfda887697949db179bc57e07ec06a0`.
- **Classificação:** **CONFIRMADO** para a atualização dos documentos e o conteúdo publicado da FAQ; **DESCONHECIDO** para download efetivo, cabeçalhos, tamanhos, hashes, licenças específicas por arquivo e mapeamento espacial.
- **Próximo passo único:** validar a resposta real do endpoint estático oficial e obter os metadados dos produtos FAFB v783.
- **Critério de aceitação:** resposta do endpoint observada e metadados concretos registrados; não iniciar importador de produção nem simulação antes da validação do esquema.


## 7.8 Correção de precisão — token de API Codex versus token CAVE (2026-10-28)

- **Motivo:** a leitura detalhada da FAQ (linhas 41–48) revelou uma nuance não capturada no registo 7.6: o exemplo programático oficial de `api/download_resource` inclui `api_token` e orienta a copiar o token da conta Codex. A FAQ descreve separadamente o token CAVE/FlyWire para operações de permissões ao vivo, como mapear root IDs e consultar histórico.
- **Correção factual:** não afirmar que o download programático pode ocorrer sem token. Os produtos estáticos são oferecidos a usuários públicos, mas o fluxo de API documentado inclui um token de API Codex. Esse token é distinto do token CAVE/FlyWire; a necessidade de autenticação no portal interativo ainda não foi testada aqui.
- **Arquivos atualizados nesta correção:** `docs/FASE_2_CIRCUITO_INICIAL.md` e `docs/ROADMAP.md`; commits `3e0ed36050bf51b376cb1f05e08eed6c91df6f72` e `ce507c406924e7436118ae52d080c5d8899d69cb`.
- **Fonte:** FAQ oficial https://codex.flywire.ai/faq, especialmente o exemplo de download programático e a distinção de tokens.
- **Acesso testado:** a ferramenta web consegue ler a FAQ, mas não abrir o recurso binário; a tentativa HTTP direta no ambiente de execução falhou por DNS. Não foi feita tentativa autenticada. **Nenhum arquivo de dados foi baixado.**
- **Segurança:** não solicitar nem colar token no chat; não o commitar nem registrar em logs. Se a autenticação for necessária, o token deve ser configurado e usado localmente pelo responsável.
- **Testes:** nenhum teste de software; documentação apenas.
- **Evidência:** **CONFIRMADO** para a instrução de uso de `api_token` no exemplo oficial; **DESCONHECIDO** para a autenticação exigida no portal interativo e para o sucesso do download real.
- **Próximo passo único:** obter os metadados e os dois produtos mínimos por um fluxo oficial autorizado, com token Codex mantido localmente se o endpoint programático o exigir.
- **Critério de aceitação:** arquivos reais recebidos e inspecionados, com tamanho, SHA-256, cabeçalhos, contagem de linhas, licença/citação e proveniência registados; só então implementar o importador de produção.


## 7.9 Upload dos três produtos FAFB v783 e validação no GitHub (2026-10-28)

- **Objetivo:** disponibilizar os três arquivos do piloto no GitHub para análise sem exigir inspeção manual local pelo utilizador.
- **Branch:** `data/fafb-v783-inputs`.
- **Pull Request:** https://github.com/heldergaraujo2/Cortex/pull/1 — aberto, não integrado na branch principal no momento deste registo.
- **Arquivos enviados:** `data/raw/fafb_v783/consolidated_cell_types.csv.gz`, `data/raw/fafb_v783/connections_princeton.csv.gz` e `data/raw/fafb_v783/coordinates.csv.gz`.
- **Resultado confirmado:** o `git push` concluiu e o GitHub aceitou os três arquivos. O servidor emitiu aviso porque `connections_princeton.csv.gz` tem 65,29 MB, acima da recomendação de 50 MB; não é um erro de envio. A pasta `data/raw` está ignorada pelo Git e foi necessário adicionar os três caminhos explicitamente com `git add -f`; nenhuma regra de ignore foi alterada.
- **Validação adicionada ao PR:** `scripts/inspect_fafb_data.py` lê os CSVs comprimidos em streaming, regista cabeçalhos, contagem de registos, tamanho, SHA-256 e duas amostras curtas de linhas; gera `fafb_v783_validation_report.json`. O workflow `.github/workflows/fafb-data-validation.yml` executa essa inspeção no GitHub Actions e publica o relatório como artefato.
- **Estado dos resultados científicos:** **DESCONHECIDO** até a execução do workflow ser concluída e o relatório ser examinado. A presença e o upload dos arquivos não confirmam integridade, esquema esperado, licença, cobertura do circuito ou conexões específicas.
- **Privacidade/segurança:** os arquivos são dados científicos públicos conforme a origem declarada pelo utilizador, mas a licença/citação específica dos produtos ainda deve ser verificada. Não há tokens incluídos no repositório.
- **Próximo passo único:** consultar a execução do workflow e analisar o relatório gerado; então verificar a correspondência de tipos e IDs para L1, Mi1, Tm3 e T4 e registrar evidências antes de implementar simulação.
- **Critério de aceitação:** relatório do GitHub Actions disponível, três arquivos lidos integralmente sem erro de gzip/CSV, cabeçalhos e contagens conhecidos, hashes registados e limitações/licença anotadas.


## 7.10 Primeira validação estrutural dos arquivos FAFB (2026-10-28)

- **Execução:** GitHub Actions FAFB v783 Data Validation, run 2, ID 40766311959; job inspect-data concluído com sucesso.
- **Resultado confirmado:** os três arquivos abriram como gzip e CSV sem erro; FILES_OK: 3/3, ERRORS: 0.
- **consolidated_cell_types.csv.gz:** 901.707 bytes; 138.327 registos de dados; colunas root_id, primary_type, additional_type(s); SHA-256 8aba246d71dc40361677493629972ce3883048c3d02010adc42bda22962a1a2d.
- **connections_princeton.csv.gz:** 68.456.801 bytes; 5.342.446 registos de dados; colunas pre_root_id, post_root_id, neuropil, syn_count, nt_type; SHA-256 445f996bf6c4b1803b9ba186189138a3061ff8623aa94c0abcf38af30a5bd48b.
- **coordinates.csv.gz:** 5.314.546 bytes; 238.909 registos de dados; colunas root_id, position, supervoxel_id; SHA-256 14337121f451f98c2576cee72c24409ada5aaf7948b7c7ca8de9040296840e05.
- **Relatório:** artefato fafb-v783-validation-report, run https://github.com/heldergaraujo2/Cortex/actions/runs/40766311959.
- **Limite da conclusão:** isto confirma integridade de leitura gzip/CSV e estrutura básica, não valida a licença específica, correspondência de todos os IDs, presença de arestas L1→Mi1/Tm3→T4, nem mecanismo funcional de seletividade direcional.
- **Análise ampliada adicionada:** o script scripts/inspect_fafb_data.py foi expandido para contar tipos primários L1/Mi1/Tm3/T4, procurar pares dirigidos entre esses grupos na tabela de conexões e medir cobertura de coordenadas. A nova execução do workflow ainda estava em andamento quando este registo foi escrito.
- **Próximo passo:** ler o resultado ampliado e verificar quais arestas e IDs estão realmente presentes antes de desenhar o importador ou a simulação.


## 7.11 Evidência estrutural real, proveniência e importador inicial (2026-10-28)

- **Branch/PR:** `data/fafb-v783-inputs`; https://github.com/heldergaraujo2/Cortex/pull/1. O PR continua aberto e não foi integrado em `main`.
- **Proveniência/licença:** o arquivo `data/raw/fafb_v783/README.md` regista origem no FlyWire Codex, snapshot FAFB v783, data de download declarada pelo responsável e licença pública indicada pelo FlyWire como CC BY-NC 4.0. Fonte oficial: https://join.flywire.ai/guidelines. O uso deve permanecer não comercial e com atribuição, sujeito às orientações oficiais.
- **Validação de dados:** execução completa do workflow FAFB v783 Data Validation, run https://github.com/heldergaraujo2/Cortex/actions/runs/40785935250, terminou com `FILES_OK: 3/3` e `ERRORS: 0`. A execução seguinte da mesma versão de inspeção também foi acionada na CI do PR.
- **Produtos e hashes confirmados pelo workflow:**
  - `consolidated_cell_types.csv.gz`: 901.707 bytes; 138.327 linhas de dados; colunas `root_id`, `primary_type`, `additional_type(s)`; SHA-256 `8aba246d71dc40361677493629972ce3883048c3d02010adc42bda22962a1a2d`.
  - `connections_princeton.csv.gz`: 68.456.801 bytes; 5.342.446 linhas; colunas `pre_root_id`, `post_root_id`, `neuropil`, `syn_count`, `nt_type`; SHA-256 `445f996bf6c4b1803b9ba186189138a3061ff8623aa94c0abcf38af30a5bd48b`.
  - `coordinates.csv.gz`: 5.314.546 bytes; 238.909 linhas; colunas `root_id`, `position`, `supervoxel_id`; SHA-256 `14337121f451f98c2576cee72c24409ada5aaf7948b7c7ca8de9040296840e05`.
- **Contagens de tipos primários:** L1=1.775; Mi1=1.581; Tm3=1.756; T4a=1.457; T4b=1.507; T4c=1.710; T4d=1.569. Total de IDs classificados no conjunto piloto L1/Mi1/Tm3/T4: 11.355.
- **Ligações dirigidas observadas na tabela** (pares `(pre_root_id, post_root_id)` distintos no conjunto todo, deduplicados entre neuropilos):
  - L1 → Mi1: 1.620 pares distintos.
  - L1 → Tm3: 6.706 pares distintos.
  - Mi1 → T4: 21.157 pares distintos.
  - Tm3 → T4: 10.351 pares distintos.
- **Cobertura de coordenadas:** 11.355/11.355 IDs do conjunto piloto têm pelo menos uma linha no arquivo de coordenadas. O arquivo tem 238.909 linhas e 139.255 IDs únicos; alguns IDs têm múltiplas linhas, que não devem ser colapsadas arbitrariamente. As unidades/semântica física de `position` não foram inferidas.
- **Mapeamento global de IDs nas conexões:** das 5.342.446 linhas, 5.318.409 têm ambos os IDs presentes no índice de tipos primários; isso não significa que os restantes estejam inválidos, pois os arquivos de anotação podem não cobrir todos os IDs da tabela.
- **Interpretação:** **CONFIRMADO** que a tabela de conectividade contém registos dirigidos para os quatro pares de tipos selecionados. **FORTEMENTE INDICADO** que estes produtos bastam para extrair um subgrafo estrutural inicial. **DESCONHECIDO** se o subgrafo, por si só, reproduz seletividade direcional ou movimento visual; faltam mapeamento espacial/colunar validado, dinâmica e comparação experimental.
- **Regra de agregação:** `connections_princeton` tem linhas por par pré/pós e neuropilo. Um par pode aparecer em mais de um neuropilo. A versão atual do script reporta linhas, pares únicos deduplicados e `syn_count` apenas dentro de cada neuropilo; não soma silenciosamente valores entre neuropilos.
- **Código adicionado:** `cortex/connectome.py` implementa carregamento estrito do subgrafo piloto, valida cabeçalhos/IDs/contagens/posições, preserva registos por neuropilo e múltiplas coordenadas. `tests/test_connectome.py` testa ingestão, separação por neuropilo, IDs não mapeados, duplicatas e dados inválidos. `scripts/import_fafb_pilot.py` gera manifesto JSON; `docs/IMPORTADOR_FAFB.md` documenta uso e limites.
- **CI confirmada:** `Cortex CI` run 61 passou em Python 3.11, 3.12 e 3.13 com 23 testes, incluindo a verificação adicional de gzip corrompido. O workflow de dados run 23 executou com sucesso a inspeção e o importador real, publicando os relatórios como artefato.
- **Próximo passo único:** iniciar a Fase 4, verificando `column_assignment.csv.gz` e o significado espacial das coordenadas antes de implementar qualquer dinâmica direcional.


## 7.12 Fecho do gate de importação estrutural do piloto (2026-10-28)

- **Workflow de dados:** https://github.com/heldergaraujo2/Cortex/actions/runs/40786637746 — sucesso; inspeção dos três arquivos e importação real concluídas.
- **Artefato de validação e manifesto:** https://github.com/heldergaraujo2/Cortex/actions/runs/40786637746/artifacts/12858733924. Inclui `fafb_v783_validation_report.json` e `fafb_v783_pilot_manifest.json`.
- **CI do pacote:** https://github.com/heldergaraujo2/Cortex/actions/runs/40786637777 — sucesso em Python 3.11, 3.12 e 3.13; 23 testes passaram, incluindo o teste de gzip corrompido.
- **Importação real:** 11.355 IDs piloto, todos com pelo menos uma linha de coordenadas; 59.218 linhas de conexão mantidas no subgrafo L1/Mi1/Tm3/T4. Tamanho e SHA-256 dos três produtos constam do manifesto.
- **Pares únicos dirigidos entre tipos principais:** L1→Mi1 1.620; L1→Tm3 6.706; Mi1→T4 21.157; Tm3→T4 10.351. Os números são pares `(pre_root_id, post_root_id)` deduplicados entre neuropilos; os registos e as contagens `syn_count` continuam preservados por neuropilo no subgrafo.
- **Conclusão da fase:** Fase 3 concluída para o importador estrutural reduzido do piloto. Não significa conectoma completo nem simulação funcional. A tabela de coordenadas não confirma sozinha o mapeamento coluna/posição visual.
- **Próxima fase:** Fase 4 — validar `column_assignment.csv.gz`, unidades e semântica das coordenadas, cobertura por subtipo T4 e só depois definir baseline espacial/dinâmica.


## 7.13 Fase 4 — preparação do validador espacial (registro histórico de 2026-10-28; gate posteriormente concluído)

- **Estado naquele momento:** Fase 4 iniciada, mas ainda NÃO concluída em 2026-10-28. A pendência foi resolvida posteriormente, conforme o registro 7.14.
- **Código novo:** `cortex/spatial.py` implementa leitor estrito para as colunas esperadas `root_id, hemisphere, type, column_id, x, y, p, q`; calcula SHA-256; valida `p/q` como inteiros e `x/y` como números finitos; conta IDs sem correspondência e cobertura por tipo primário; distingue colunas por `(hemisphere, column_id)`.
- **CLI:** `scripts/inspect_fafb_columns.py` combina o arquivo de colunas com as anotações primárias existentes e produz um relatório JSON fora do Git por padrão.
- **Testes sintéticos:** `tests/test_spatial.py` cobre cobertura por tipo, hemisférios, IDs sem correspondência, cabeçalhos ausentes, `p/q` inválidos, coordenadas `x` inválidas, arquivo ausente e gzip corrompido. Estes testes verificam o código, não a exportação biológica real.
- **CI confirmada para o código novo:** `Cortex CI` run 70 passou com **33 testes** em Python 3.11, 3.12 e 3.13; o log do job Python 3.13 reporta `33 passed in 0.14s`. `Cortex CI` run 72 também terminou com sucesso no commit `66b238f0b66adefae471707872f8747c7b781886`. Isso valida o software sintético, não os dados reais de colunas.
- **CI:** `.github/workflows/fafb-data-validation.yml` foi ampliado para executar os testes e inspecionar a tabela real quando ela estiver presente; se faltar, emite warning e deixa o gate empírico pendente.
- **Documentação:** `docs/VALIDACAO_ESPACIAL.md` explica esquema, limites e distinção entre `x/y` e `p/q`; `docs/ROADMAP.md` agora exige explicitamente a validação do arquivo original.
- **Referência de coordenadas:** o FAQ do Codex descreve a visualização FlyWire em voxels de 4 × 4 × 40 nm, mas isso não basta para inferir automaticamente unidades/semântica dos campos `x/y` de `column_assignment`. Não foi aplicada transformação nem conversão.
- **Evidência:** **CONFIRMADO** que o parser, CLI, testes e workflow foram adicionados à branch; **DESCONHECIDO** a cobertura real, os tipos presentes, a distribuição de colunas e as relações espaciais até ler o arquivo original.
- **Gate bloqueador / próximo passo naquele registo:** disponibilizar `column_assignment.csv.gz`. **RESOLVIDO posteriormente:** ver seção 7.14, que registra upload, SHA-256, cobertura real e conclusão do gate em 2026-11-04.


## 7.14 Fecho da validação espacial e início da baseline dinâmica (2026-11-04)

### Fecho da Fase 4 — evidência real

- **CONFIRMADO:** `column_assignment.csv.gz` foi enviado à branch `data/fafb-v783-inputs` no commit `235e01bbb6360af977f8a0b2533ae2793340597e`; tamanho 462.838 bytes.
- **CONFIRMADO:** execução FAFB v783 Data Validation #36, commit `235e01bbb6360af977f8a0b2533ae2793340597e`, terminou com sucesso: https://github.com/heldergaraujo2/Cortex/actions/runs/41942497302.
- **CONFIRMADO:** Cortex CI #74 passou em Python 3.11, 3.12 e 3.13: https://github.com/heldergaraujo2/Cortex/actions/runs/41942497333.
- **Relatório espacial real:** 45.528 linhas e 45.528 root IDs únicos; zero IDs sem correspondência com a tabela de tipos primários; 1.581 pares únicos (hemisfério, column_id), sendo 785 no hemisfério esquerdo e 796 no direito.
- **Cobertura dos 11.355 IDs do piloto:** 10.637 com atribuição e 718 sem atribuição. Cobertura: L1 88,56%; Mi1 100%; Tm3 85,36%; T4a 98,90%; T4b 99,07%; T4c 90,82%; T4d 95,47%.
- **SHA-256 de column_assignment:** `bdf4ce7f62cc63493d53eefad3816ff2dfd08b190e97b35a492e0e453df2f0f6`.
- **Limite:** o relatório preserva x/y e p/q sem inferir unidades, projeção ou transformação retinotópica. Cobertura espacial não prova seletividade direcional nem completude biológica do circuito.
- **Conclusão:** Fase 4 concluída para ingestão, integridade estrutural e cálculo de cobertura espacial/colunar do piloto. Sem afirmar interpretação física dos campos x/y nem funcionalidade visual.

### Início da Fase 5 — implementação da baseline v0

- **Código adicionado:** `cortex/dynamics.py` com taxa abstrata limitada a [0,1], atualização síncrona determinística e grafo restrito a um neuropilo por execução.
- **Regra de pesos:** `syn_count` normalizado pela soma de entradas de cada neurónio pós-sináptico, dentro do neuropilo escolhido. É uma hipótese de engenharia, não eficácia sináptica medida.
- **Controles:** pulso ON sintético, ausência de estímulo, ablação de Mi1 e ablação de Tm3. Plasticidade desligada.
- **Métricas:** série temporal da taxa média T4, pico, passo do pico e séries por subtipo T4a–T4d.
- **CLI:** `scripts/run_fafb_baseline.py`; os neuropilos ME_L e ME_R são executados separadamente e nunca somados.
- **Testes:** `tests/test_dynamics.py` cobre propagação em dois estágios, determinismo, controlo zero, limites de estado, validação de parâmetros, separação por neuropilo e ablações.
- **Documento:** `docs/FASE_5_BASELINE_DINAMICA.md`.
- **Workflow:** `.github/workflows/fafb-data-validation.yml` foi atualizado para executar a baseline real ME_L e ME_R e publicar os dois relatórios.
- **HIPÓTESE DE ENGENHARIA:** a dinâmica rate-based e a normalização estrutural são uma baseline mínima útil para testar propagação.
- **DESCONHECIDO:** se parâmetros/dinâmica representam neurónios biológicos; se o subcircuito reduzido reproduz comportamento visual; se há seletividade direcional. Esta baseline não testa movimento, espaço visual, sinal neurotransmissor ou aprendizagem.
- **Estado da Fase 5 neste registo:** implementação adicionada, execução real/CI ainda pendente. Não marcar como concluída até verificar os workflows e examinar os relatórios ME_L/ME_R.
- **Próximo passo prioritário:** acompanhar as execuções CI do commit mais recente, corrigir qualquer falha e analisar os dois relatórios reais. Não integrar PR #1 nem alterar `main`.


## 7.15 Revisão metodológica da baseline v0 (2026-11-04)

- **Primeira execução real:** FAFB Data Validation run #41, commit `ee3a9b48f81eb74d14269201ebcf7b79a3bd9f96`, terminou com sucesso e gerou relatórios ME_L/ME_R.
- **Revisão crítica do artefato:** o pulso propagou até T4 e o controlo sem estímulo ficou em zero, mas a comparação das ablações não era válida: ao remover Mi1/Tm3, a versão inicial renormalizava os pesos restantes e alterava o conjunto de T4 medido.
- **Decisão:** os resultados de ablação do run #41 ficam supersedidos e não devem sustentar inferências.
- **Correção:** pesos normalizados uma única vez no grafo intacto; ablações removem a via sem renormalizar as restantes. A população T4 de leitura permanece idêntica em todos os cenários; T4 sem entradas após ablação conta como zero. Adicionado teste que verifica explicitamente estas duas propriedades.
- **Estado naquele momento:** nova CI e execução real ainda pendentes. **Resolvido posteriormente:** Fase 5 corrigida e validada no registro 7.16; usar os resultados finais dessa seção, não os do run #41.


## 7.16 Fecho da Fase 5 — baseline estrutural rate-based v0 (2026-11-04)

- **Commit validado:** `2868cd7046fd474bcb1cf7bc33dc818454fd9aa9` na branch `data/fafb-v783-inputs`.
- **Cortex CI #86:** sucesso em Python 3.11, 3.12 e 3.13; 45 testes aprovados em cada versão. https://github.com/heldergaraujo2/Cortex/actions/runs/41943528569
- **FAFB Data Validation #48:** sucesso; inspeção dos dados, testes, baseline ME_L e baseline ME_R concluídos; artefato publicado. https://github.com/heldergaraujo2/Cortex/actions/runs/41943528584
- **Artefato:** contém `fafb_v783_validation_report.json`, `fafb_v783_pilot_manifest.json`, `fafb_v783_column_assignment_report.json`, `fafb_v783_baseline_ME_L.json` e `fafb_v783_baseline_ME_R.json`.
- **ME_L:** 19.841 arestas elegíveis; população T4 fixa de 6.243, com 3.131 recebendo entrada modelada no grafo intacto; pico médio T4 0,188023 no passo 4; controlo sem estímulo 0; ablação Mi1 0,036454 (queda 80,61%); ablação Tm3 0,151570 (queda 19,39%).
- **ME_R:** 19.970 arestas elegíveis; população T4 fixa de 6.243, com 3.102 recebendo entrada modelada no grafo intacto; pico médio T4 0,185258 no passo 4; controlo sem estímulo 0; ablação Mi1 0,035259 (queda 80,97%); ablação Tm3 0,149999 (queda 19,03%).
- **Correção metodológica aplicada:** os pesos são normalizados uma vez no grafo intacto; ablações removem vias sem renormalizar as restantes; a população T4 de leitura é invariável entre cenários e inclui taxa zero quando uma célula perde todas as entradas modeladas.
- **CONFIRMADO:** propagação abstrata determinística até T4 para pulso global em L1; controlo zero; comportamento reprodutível e testes aprovados.
- **HIPÓTESE DE ENGENHARIA:** a assimetria entre ablações é uma propriedade desta representação estrutural e da regra de pesos.
- **DESCONHECIDO:** se essa assimetria reflete contribuições biológicas reais; parâmetros e pesos não são fisiologicamente calibrados.
- **NÃO DEMONSTRADO:** estímulo espacial, movimento, seletividade direcional, aprendizagem ou comportamento.
- **Conclusão:** Fase 5 concluída como baseline computacional estrutural v0, não como modelo biológico validado.
- **Próxima fase:** Fase 6 — verificar a semântica/orientação de p/q e column_id em fontes oficiais; só depois construir estímulos espaço-temporais em direções opostas, flash estático e controlo sem estímulo, mantendo as alegações de direção bloqueadas até validação.


## 7.17 Início da Fase 6 — coordenadas e frentes espaço-temporais (2026-11-04)

- **Branch:** `data/fafb-v783-inputs`; PR #1 aberto, `main` não integrada.
- **Fontes primárias consultadas:** Seung (Nature 2024, DOI 10.1038/s41586-024-07953-5), Zhao et al. (Nature 2025, DOI 10.1038/s41586-025-09276-5), Borst et al. (2020, DOI 10.1007/s00359-019-01375-9), Salazar-Gatzimas et al. (Neuron 2018, DOI 10.1016/j.neuron.2017.03.010), FAQ oficial Codex.
- **CONFIRMADO pela literatura FAFB:** p/q são coordenadas discretas da malha hexagonal da medula; +p anterodorsal, +q posterodorsal e +v dorsal. Projeções de ordenação: p = 2p-q; q = 2q-p; v = p+q.
- **CONFIRMADO pela literatura:** a malha da retina é esquerda-direita invertida em relação à medula pelo quiasma óptico. A conversão de medula para espaço visual requer eye map e geometria local; não será inventada.
- **DESCONHECIDO:** semântica/unidades específicas de x/y na tabela column_assignment; não são usadas no experimento.
- **Implementação adicionada:** `cortex/visual_stimuli.py` gera frentes L1 ordenadas por p/q/v e as direções opostas como reversões exatas. `cortex/dynamics.py` recebeu simulador de agenda de entradas. `scripts/run_fafb_spatiotemporal.py` produz relatórios ME_L/ME_R com frentes opostas, flash ON e controlo sem estímulo. `tests/test_visual_stimuli.py` cobre projeções, reversibilidade, energia igual, separação de hemisfério, duplicatas e propagação agendada.
- **Desenho experimental:** cada L1 atribuído é ativado exatamente uma vez por direção; a direção oposta tem os mesmos frames em ordem inversa. As métricas de assimetria são apenas diagnósticas, não DSI biológico.
- **Limite crítico:** a rede atual contém L1/Mi1/Tm3/T4, sem entradas inibitórias Mi4/Mi9/C3/CT1, sem atrasos fisiológicos e sem dinâmica de membrana. Não permite alegar seletividade direcional. T4a–T4d serão reportados, mas não mapeados a direções cardinais globais.
- **Próximo gate:** CI real após implementação, inspeção dos relatórios espaciais dos dois hemisférios e correção de qualquer falha. Só então preparar os primeiros testes locais no PC.


## 7.18 Revisão do readout espacial e correção (2026-11-05)

- **Primeira execução espacial:** FAFB Data Validation #56, commit `1ac921ee5e6a0cc021eecf2e24df1c54146455a8`, terminou com sucesso e gerou relatórios ME_L/ME_R.
- **Auditoria do artefato:** detectado que o estímulo usava L1 atribuídos a um hemisfério, mas a média T4 incluía a população bilateral. A cobertura L1 por hemisfério também estava sendo calculada com denominador bilateral.
- **Decisão:** valores de resposta e assimetria do run #56 são supersedidos; não usar para inferência.
- **Correção:** função `assigned_t4_readout_by_hemisphere` seleciona apenas T4a–T4d atribuídos ao hemisfério do neuropilo, valida concordância com o tipo primário e rejeita duplicatas. A cobertura L1 global (88,56%) é separada da contagem atribuída por hemisfério; não se inventa cobertura específica para neurónios sem atribuição.
- **Testes novos:** seleção de T4 por hemisfério, tipo inconsistente e duplicatas. A nova suíte CI deve validar a alteração.
- **Estado:** Fase 6 permanece em andamento até nova CI, execução real ME_L/ME_R e inspeção dos artefatos corrigidos.


- **Progressão da frente:** bins inteiros vazios entre colunas são mantidos como frames sem estímulo; não se comprimem lacunas. Um passo é uma unidade de projeção da malha, não tempo biológico ou distância física.


## 7.19 Fase 6 — preparação no repositório concluída; primeiro teste no PC (2026-11-05)

- Commit validado: `784f30d43811da795fbda5ddadcbb5599ef91a8c` na branch `data/fafb-v783-inputs`.
- FAFB Data Validation #71: sucesso; importação, validação espacial, testes, baseline ME_L/ME_R e frentes espaço-temporais ME_L/ME_R concluídos. https://github.com/heldergaraujo2/Cortex/actions/runs/41945748140
- Cortex CI #109: 61 testes aprovados em Python 3.11, 3.12 e 3.13. https://github.com/heldergaraujo2/Cortex/actions/runs/41945747960
- Readout corrigido: somente T4 atribuídos ao mesmo hemisfério do neuropilo; 2.986 T4 left e 2.999 T4 right. O artefato antigo com readout bilateral fica supersedido.
- Resultado: assimetria integrada +/− de 0,044% a 0,978%; flash ON integrado próximo de 0,99; ausência de estímulo zero. É um diagnóstico de engenharia, não DSI nem seletividade biológica.
- Limites mantidos: sem conversão para direções do campo visual, sem mapeamento preferencial global de T4a–T4d, sem inibição ou dinâmica fisiológica calibrada.
- Script local criado: `scripts/run_first_pc_validation.ps1`. Confere branch, alterações staged/não staged, sincronização com origin e arquivos de dados; usa ambiente virtual local e grava relatórios em `artifacts/pc-validation` (ignorado pelo Git). Não executa reset, clean, stash nem altera arquivos brutos.
- Estado da Fase 6: gates do repositório/GitHub concluídos. Primeiro teste no PC ainda não executado.
- Próxima ação: sincronizar a branch com segurança no clone Windows e executar o script local. Não avançar para a expansão do modelo até examinar a saída local.


## 7.20 Fase 8 — referência anatômica M1 e CI concluída (2026-11-05)

- Branch isolada: `research/phase-8-anatomical-column-reference`, baseada em `data/fafb-v783-inputs` no commit `66cb821590090561c69679cd5c2c005413bde50a`.
- Documento: `docs/FASE_8_REFERENCIA_ESPACIAL_M1.md`; commit atual `e4873cd702a411ed771b8b4ee25494cd9448d85f`.
- PR #2 Draft: https://github.com/heldergaraujo2/Cortex/pull/2. PR #1 e `main` permanecem sem alterações.
- Cortex CI #189: sucesso no commit atual, Python 3.11, 3.12 e 3.13; os três jobs concluíram os testes e a demonstração sintética. https://github.com/heldergaraujo2/Cortex/actions/runs/42040581437
- A execução #189 não publicou artefatos. O CI confirma a integridade da alteração documental, não valida o crosswalk CATMAID→FlyWire nem a geometria da grade.
- Inspeção adicional do repositório público `reiserlab/eyemap_T4`: `data/neu_Mi1.RData` existe na branch `main` (blob SHA `ee941396f53e813b0e12d5a1fcc64abdfec321db`), mas a interface de leitura textual não expôs o conteúdo binário. Os objetos RData continuam por inspecionar em ambiente R/pyreadr; não declarar IDs ou cobertura dos 780 Mi1 como confirmados.
- **CONFIRMADO:** CI #189 aprovado em três versões de Python; scripts públicos referenciam os objetos RData e usam centros M10 de Mi1 para construir a referência anatômica.
- **DESCONHECIDO:** dimensões, alinhamento dos índices, IDs CATMAID por Mi1, cobertura dos 780 neurônios e crosswalk para FAFB v783.
- **Próximo gate:** obter os RData sem perda, inspecionar estrutura/rownames/listas e produzir inventário de identidade reproduzível. Só depois executar crosswalk CATMAID→FlyWire e validar correspondência de snapshot.

- **Refinamento de evidência no código dos autores:** `Fig_2_EM.R` indexa `Mi1_M10_xyz` por `Mi1_neu_ind[match(anno_Mi1_DRA$skid, anno_Mi1$skid)]`; `proc_eyemap.R` carrega `Mi1_M10_xyz` de `neu_Mi1.RData`. Isso confirma que o código usa uma cadeia explícita CATMAID `skid` → índice local → linha de coordenada M10 para as anotações mostradas. Cobertura total, unicidade e crosswalk para FAFB v783 continuam desconhecidos. Detalhamento atualizado em `docs/FASE_8_REFERENCIA_ESPACIAL_M1.md`.


## 7.21 Ferramenta Gate 8A adicionada (2026-11-05)

- Adicionado `scripts/inspect_mi1_reference.R` na branch isolada da Fase 8. A ferramenta lê `neu_Mi1.RData` e `Mi1_ind.RData` em ambiente R separado, inventaria objetos e gera tabelas da cadeia `anno_Mi1$skid` → `Mi1_neu_ind` → `Mi1_M10_xyz`, incluindo resumo de duplicatas, índices válidos e coordenadas finitas.
- Atualizado `docs/FASE_8_REFERENCIA_ESPACIAL_M1.md` com instruções PowerShell e limites do script.
- **Não executado:** os binários RData não foram disponibilizados pelo conector GitHub (o blob gzip falhou na decodificação UTF-8; download direto indisponível). Portanto, não há contagens ou resultados empíricos novos. O script não altera os arquivos de origem e não chama CATMAID/FlyWire.
- Último commit: `a81cd152733e5eb0e7ac495852e932ac3d3d51c6`. PR #2 incorpora automaticamente os commits desta branch; permanece Draft. `main` e PR #1 preservados.
- Próxima ação: executar o script contra os dois RData originais em ambiente R 4.4.1, revisar `mapping_summary.csv` e os casos não mapeados, depois decidir se o Gate 8A passa. Não iniciar crosswalk 8B antes disso.
