# Arquitetura Híbrida e Cortex Coletivo

**Versão:** 1.0 — decisão arquitetural inicial  
**Data:** 2026-10-28  
**Estado:** arquitetura aprovada como hipótese de engenharia; ainda não implementada nem validada em execução.  
**Escopo:** quatro instâncias completas do cérebro/connectoma de referência, com especialização experimental, coordenação e memória coletiva.

## 1. Decisão principal

O Cortex será projetado para experimentar **quatro instâncias completas e independentes** do mesmo connectoma de referência. Cada instância representa uma simulação integral da estrutura neural escolhida, não apenas um fragmento do grafo. As quatro instâncias terão estados dinâmicos separados e poderão desenvolver especializações por meio de tarefas, entradas e condições experimentais diferenciadas.

Esta é uma arquitetura de software para investigação. Não significa que quatro cópias de um connectoma de mosca formem biologicamente quatro cérebros humanos, nem garante inteligência superior. O benefício coletivo é uma hipótese a medir.

**Importante:** “clone completo” significa uma instância que contém a representação completa do connectoma escolhido. Não significa que o connectoma, sozinho, seja um cérebro funcional completo: dinâmica, parâmetros, entradas, saídas, plasticidade e memória ainda precisam de ser implementados e validados.

## 2. Quatro instâncias e responsabilidades

A primeira configuração experimental terá exatamente quatro cérebros:

| ID | Nome de trabalho | Responsabilidade primária | Responsabilidades secundárias |
|---|---|---|---|
| C1 | Cortex Coordenador | Coordenar objetivos, distribuir tarefas, reunir resultados e identificar conflitos entre propostas | Participar nas tarefas comuns e manter visão global do estado coletivo |
| C2 | Cortex Perceptivo | Especializar-se em interpretar estímulos e identificar padrões | Enviar observações, incertezas e evidências à memória coletiva |
| C3 | Cortex Aprendizagem | Investigar aquisição de competências, plasticidade e transferência de experiências | Propor experiências e avaliar retenção/interferência |
| C4 | Cortex Ação | Investigar seleção de respostas e consequências de ações em ambientes controlados | Avaliar resultados comportamentais e devolver feedback |

Estas atribuições são **hipóteses de organização experimental**, não alegações de que a anatomia da mosca contenha quatro módulos correspondentes a estes nomes. As especializações devem ser revistas quando o dataset e os circuitos reais forem selecionados.

Cada instância continuará a conter a mesma estrutura conectômica de referência no primeiro experimento. A especialização inicial será obtida principalmente por objetivos, tarefas, entradas, experiências e políticas de treino distintas — não por apagar ou reescrever arbitrariamente partes do conectoma.

## 3. Um cérebro coordenador: benefícios e riscos

### Benefícios esperados
- Um ponto claro para organizar tarefas e consolidar respostas.
- Menos duplicação de trabalho, com atribuições e estados de tarefa explícitos.
- Uma interface para resumir divergências, prioridades e resultados.
- Facilitar a avaliação do grupo contra cada cérebro isolado.

### Riscos
- O coordenador pode tornar-se um gargalo de desempenho.
- Se for a única autoridade, um erro seu pode contaminar todo o resultado coletivo.
- As outras instâncias podem deixar de contribuir se o coordenador filtrar excessivamente a informação.
- Uma única instância falhar pode interromper a coordenação.
- Uma hierarquia central pode reduzir a diversidade útil ou suprimir hipóteses minoritárias.

### Decisão de engenharia
C1 será o **cérebro coordenador**, mas não terá autoridade irrestrita nem será a única fonte de verdade. Um componente convencional e determinístico de orquestração do software ficará responsável por contratos de mensagens, limites de recursos, timeouts, registo de eventos, validação de formato e recuperação de falhas. Esse componente não será contado como um quinto cérebro e não deve substituir o núcleo neural nas avaliações.

C1 poderá propor prioridades, delegar tarefas e sintetizar resultados. As decisões coletivas importantes devem preservar as contribuições e evidências de C2–C4, indicar divergências e permitir comparação com uma agregação sem coordenador. Se C1 falhar, o orquestrador deve conseguir colocar o sistema em estado seguro e permitir retomar ou repetir a coordenação.

**Hipótese a testar:** um coordenador melhora a eficiência e a consistência em relação a uma organização sem coordenador. Não assumir que isso já está demonstrado.

## 4. Memória coletiva partilhada

As quatro instâncias utilizarão uma **memória coletiva partilhada**, acessível a todas. Esta decisão atende ao objetivo de permitir que experiências e descobertas de uma instância possam ajudar as outras.

A memória será um subsistema explícito do software, não automaticamente uma memória neural biologicamente emergente.

### Tipos de conteúdo
1. **Memória de trabalho coletiva:** tarefas ativas, objetivos, contexto comum, estado de coordenação e resultados ainda em análise.
2. **Memória episódica:** registo de experiências, estímulos, ações, resultados, falhas e condições experimentais.
3. **Memória de conhecimento:** informações consolidadas, relações, hipóteses, confiança, fontes e condições em que foram verificadas.
4. **Memória de competências/artefactos:** políticas, parâmetros ou artefactos aprendidos, sempre versionados e com proveniência.
5. **Registo de conflitos:** afirmações incompatíveis, alternativas e evidências necessárias para as resolver.

### Regras para evitar conflitos e corrupção
- A memória coletiva terá registo de origem: instância, tarefa, data lógica, versão, evidências e nível de confiança.
- Não substituir silenciosamente uma informação contraditória. Guardar ambas as versões, marcar o conflito e executar um processo explícito de resolução.
- Diferenciar observação, hipótese, conclusão experimental e informação ainda não verificada.
- Usar escrita versionada e operações atómicas; evitar que duas instâncias sobrescrevam a mesma entrada sem deteção de conflito.
- O coordenador pode propor consolidação, mas a proveniência e as versões anteriores devem permanecer recuperáveis.
- Resultados experimentais brutos e eventos devem ser preservados separadamente de resumos consolidados.
- Cada experimento deve poder ser reproduzido com a memória coletiva desativada, congelada ou limitada, para medir o seu contributo.

### O que será partilhado e o que continuará separado
**Partilhado:** contexto, experiências registadas, observações, resultados, conhecimento validado, tarefas, relatórios e artefactos selecionados.

**Separado por instância, pelo menos inicialmente:** estado neural dinâmico, estado transitório da simulação e parâmetros plásticos individuais. A partilha ou sincronização desses estados será uma experiência posterior, pois copiá-los automaticamente pode apagar a diversidade e causar interferência entre aprendizagens.

Assim, todas as instâncias consultam a mesma memória coletiva sem serem obrigadas a ter estados neurais idênticos. Partilhar memória não significa fundir os quatro cérebros numa única instância.

## 5. Protocolo de cooperação

O ciclo inicial proposto é:

1. O orquestrador regista o objetivo e cria uma tarefa identificada.
2. C1 propõe uma distribuição de tarefas entre C2, C3 e C4, podendo também executar trabalho próprio.
3. Cada instância recebe o contexto comum relevante e executa a sua tarefa com estado neural próprio.
4. Cada resultado é publicado na memória coletiva com origem, configuração, evidências, incertezas e resultado.
5. C1 prepara uma síntese que preserva desacordos e resultados minoritários.
6. O orquestrador verifica contratos, completude e limites operacionais.
7. A síntese é comparada com resultados individuais e, quando apropriado, com uma estratégia de agregação sem coordenador.
8. O resultado e as métricas são registados para avaliação posterior.

Não enviar apenas conclusões resumidas quando os dados de suporte são necessários para auditar o resultado. Não permitir que uma instância altere diretamente o estado interno das outras sem um protocolo experimental explícito.

## 6. Especialização sem pressupostos excessivos

A especialização não será considerada existente só porque uma instância recebeu um nome ou um prompt diferente. Será medida por resultados em tarefas definidas previamente.

Para cada especialização:
- definir tarefas de treino e teste;
- registar entradas, condições, parâmetros e sementes;
- comparar com instâncias sem especialização;
- verificar se a especialização melhora uma tarefa e se prejudica outras;
- medir transferência de conhecimento e interferência;
- manter uma baseline em que as quatro instâncias recebem as mesmas tarefas;
- permitir alterar as atribuições se os dados indicarem uma divisão melhor.

A organização por papéis poderá mudar depois da auditoria científica. Os quatro cérebros permanecem como decisão de arquitetura experimental inicial; a correspondência exata entre papéis e circuitos permanece aberta.

## 7. Plano de validação incremental

1. **Baseline individual:** executar um circuito pequeno e validado; medir tempo, RAM, VRAM e resultados.
2. **Instância completa de referência:** ampliar a representação apenas após a medição e validação dos componentes.
3. **Segunda instância independente:** confirmar que dois estados independentes podem ser executados e reproduzidos.
4. **Quatro instâncias sem cooperação:** medir custo agregado e diversidade de resultados.
5. **Memória partilhada apenas para leitura:** verificar que todas conseguem consultar o mesmo repositório sem alterar dados indevidamente.
6. **Memória partilhada com escrita versionada:** testar concorrência, proveniência, conflitos e recuperação.
7. **Cooperação sem coordenador:** estabelecer uma baseline coletiva.
8. **Cooperação com C1 coordenador:** comparar qualidade, latência, custo, conflitos e robustez.
9. **Especialização diferenciada:** comparar tarefas especializadas com condições idênticas e com tarefas distribuídas.
10. **Teste de falha do coordenador:** verificar recuperação segura e preservação dos resultados.
11. **Escala e otimização:** decidir com base em profiling se as instâncias devem correr no mesmo processo, em processos separados ou em hardware distinto.

Não executar quatro conectomas completos antes de medir o custo e validar uma implementação pequena. A sequência de implementação não muda: auditoria do ambiente primeiro.

## 8. Métricas obrigatórias

- Qualidade da tarefa por instância e em conjunto.
- Melhoria sobre a melhor instância individual.
- Melhoria sobre uma agregação simples sem coordenador.
- Tempo total e latência de coordenação.
- RAM, VRAM, CPU e armazenamento.
- Quantidade de trabalho duplicado.
- Frequência e gravidade de conflitos na memória.
- Recuperação após falha de uma instância.
- Diversidade de soluções e retenção de conhecimento.
- Interferência entre aprendizagem individual e memória partilhada.
- Reprodutibilidade com as mesmas configurações e sementes.

A alegação de que o coletivo é melhor só será sustentada se os resultados comparativos o demonstrarem. Maior throughput por paralelismo deve ser distinguido de melhoria da qualidade de cada resposta.

## 9. Limites científicos e técnicos

- As quatro instâncias são simulações computacionais, não quatro cérebros biológicos.
- O connectoma não fornece automaticamente toda a dinâmica neuronal nem regras completas de aprendizagem.
- O cérebro coordenador é uma função experimental atribuída a uma instância, não uma região cerebral identificada na mosca.
- A memória partilhada é uma camada de software explicitamente modelada.
- A especialização, a transferência de conhecimento e o ganho de inteligência coletiva são hipóteses.
- O custo de quatro instâncias não pode ser calculado com rigor antes do profiling do simulador e do hardware.
- Não alegar inteligência geral, consciência ou capacidade humana com base apenas na arquitetura.

## 10. Critérios de aceitação desta arquitetura

A arquitetura será considerada implementada — não apenas documentada — quando:
- existirem contratos de configuração e identidade para exatamente quatro instâncias;
- cada instância puder manter estado neural independente;
- a memória coletiva tiver esquema, proveniência, versionamento e testes de concorrência;
- o coordenador puder delegar e consolidar resultados sem apagar divergências;
- o orquestrador suportar timeouts e falhas sem corromper memória;
- existirem testes e benchmarks individuais, coletivos, com e sem coordenador e com memória partilhada ligada/desligada;
- os resultados e custos forem registados e reproduzíveis.

Até lá, esta documentação define a decisão e o plano de investigação, não uma capacidade já disponível.
