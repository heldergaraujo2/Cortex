# Fase 2 — circuito inicial e tarefa experimental

**Estado:** Fase 2 de seleção e desenho experimental concluída. Circuito e tarefa foram selecionados por regra reproduzível; extração/validação de dados permanece como gate explícito da Fase 3. Não confundir seleção reproduzível por tipo celular com extração validada de dados.

## 1. Decisão

Selecionar como **circuito piloto exploratório da via ON de deteção de movimento** o núcleo:

`L1 → Mi1/Tm3 → T4`

- `L1`: interneurónio da lâmina que encaminha sinais ON para a via visual.
- `Mi1` e `Tm3`: vias medulares pré-sinápticas que fornecem entradas importantes a T4.
- `T4`: neurónio associado à via ON de movimento e à seletividade direcional.

Esta é uma redução deliberada, não uma alegação de que estes são os únicos elementos do circuito biológico. A literatura de conectómica identifica Mi1 e Tm3 como entradas importantes de T4, mas também descreve entradas adicionais e incertezas quanto ao mecanismo funcional. A reconstrução completa de entradas T4 inclui outros tipos como Mi4, Mi9, C3, TmY15 e CT1. Esses tipos devem ser contabilizados no relatório de cobertura e podem exigir inclusão numa versão ampliada.

**Fontes primárias:**
- Takemura et al., *A visual motion detection circuit suggested by Drosophila connectomics*, Nature (2013): https://www.nature.com/articles/nature12450
- Shinomiya et al., *The comprehensive connectome of a neural substrate for ‘ON’ motion detection in Drosophila*, eLife (2017): https://elifesciences.org/articles/24394
- Codex FAQ — snapshots, tabelas estáticas, filtros e campos: https://codex.flywire.ai/faq
- Dorkenwald et al., *Neuronal wiring diagram of an adult brain*, Nature (2024): https://www.nature.com/articles/s41586-024-07558-y

## 2. Delimitação reproduzível

Dataset fixo: **FlyWire FAFB v783 (snapshot de outubro de 2023)**.

Após descarregar os CSV comprimidos oficiais e inspecionar os cabeçalhos reais:

1. Construir um índice de neurónios por ID estável (`root_id`) e tipo celular resolvido, preservando também anotações alternativas e a proveniência.
2. Selecionar células anotadas como `L1`, `Mi1`, `Tm3` e `T4`; registar as variantes de anotação existentes em vez de normalizar silenciosamente.
3. Selecionar arestas dirigidas cujos pares pré/pós-sinápticos liguem `L1 → Mi1`, `L1 → Tm3`, `Mi1 → T4` ou `Tm3 → T4`.
4. Para a primeira análise, utilizar a tabela de conectividade Princeton com limiar documentado pelo snapshot (Codex declara o limiar padrão FAFB de 5+ sinapses por par). Preservar contagens e neuropilos; não somar duplicados por neuropilo sem registar a regra de agregação.
5. Produzir um relatório de cobertura com número de neurónios e arestas por classe, neurónios sem anotação, conexões ausentes e caminhos incompletos.
6. Manter os IDs concretos e os hashes do material importado num manifesto gerado depois do download. Não inventar IDs nem assumir que todas as células esperadas existem no snapshot.

A extração deve falhar com uma mensagem clara se os campos necessários não forem encontrados. Os nomes acima são filtros semânticos pretendidos; os nomes de coluna exatos só ficam confirmados após inspeção dos ficheiros oficiais.

## 3. Tarefa do primeiro experimento

**Pergunta:** um modelo explícito e reproduzível deste subcircuito consegue distinguir uma sequência sintética de luminância ON em movimento de estímulos estáticos ou apresentados na direção oposta?

### Entradas
- Sequência temporal de estímulos sintéticos de luminância ON em posições adjacentes.
- Condições: movimento numa direção, movimento na direção oposta, flash estático e controlo sem estímulo.
- A relação entre posições visuais e neurónios/colunas só será usada se a tabela espacial adequada for encontrada, verificada e citada. Sem essa correspondência, o teste limita-se à topologia do grafo e não poderá ser descrito como teste de movimento espacial.

### Saídas observáveis
- Atividade simulada de cada T4 incluído e agregação por subtipo/direção, quando anotada.
- Resposta máxima, latência e diferença entre as condições direcionais, conforme as unidades temporais escolhidas e documentadas.
- Cobertura do circuito e fração de entradas T4 conhecidas que ficaram fora do modelo.

### Baselines e controlos
1. Baseline sem seletividade: soma ponderada/contagem de entradas, sem atrasos nem não linearidade.
2. Baseline temporal: filtros temporais simples sem conectoma individual.
3. Modelo reduzido com conectividade, mas sem plasticidade.
4. Ablations que removem separadamente a via Mi1 ou Tm3.
5. Controlo de direção invertida, flash estático e entradas aleatórias com a mesma energia.

Os modelos simplificados são baselines computacionais, não modelos biológicos confirmados.

### Métrica primária
Diferença de resposta entre direções opostas, normalizada pela resposta média e acompanhada de intervalo de incerteza. A métrica só é aplicável depois de existir uma correspondência validada entre posição visual, entradas e direção preferida de T4. Métricas secundárias: separação entre movimento e flash estático, latência, estabilidade a sementes e custo de execução.

### Critério de sucesso pré-registado
Antes da simulação real, escolher e documentar um limiar numérico de seletividade e a forma de o calcular, usando uma baseline sintética para validar o código. O limiar não será escolhido retroativamente para favorecer o modelo. Nenhuma afirmação de sucesso biológico será feita sem comparação com resultados experimentais publicados compatíveis.

## 4. Parâmetros e limites

O conectoma fornece estrutura e contagens de conexões, mas não determina por si só todos os pesos funcionais, sinais fisiológicos, atrasos, constantes de membrana ou regras de plasticidade. Cada parâmetro deve ser marcado como:
- observado no dado;
- anotação/previsão;
- estimativa baseada na literatura;
- escolha de engenharia;
- desconhecido.

Não ativar plasticidade na primeira baseline. Primeiro verificar se o grafo importado, o modelo dinâmico escolhido e a tarefa básica produzem resultados determinísticos e interpretáveis.

## 5. Produtos de dados e acesso

O FAQ oficial do Codex recomenda os downloads CSV estáticos para processamento em lote e apresenta um exemplo oficial que usa os produtos `consolidated_cell_types` e `connections_princeton`. A tabela de conexões é dirigida e pode conter múltiplas linhas para o mesmo par em neuropilos distintos. O limiar padrão do FAFB é 5+ sinapses por par.

Portal: https://codex.flywire.ai/api/download?dataset=fafb  
FAQ e notebook de acesso programático: https://codex.flywire.ai/faq  
A obtenção de recursos requer um token de conta Codex; não guardar token em Git, logs, testes ou memória do projeto.

Antes da importação, confirmar no portal os produtos exatos, tamanhos, cabeçalhos, citações e termos aplicáveis. A licença geral publicada para FAFB v783 é CC BY-NC 4.0: atribuição obrigatória e uso não comercial. Confirmar as condições no produto concreto no momento da obtenção.

## 6. O que esta decisão não prova

- Não prova que o subcircuito reduzido é suficiente para reproduzir a seletividade direcional.
- Não prova que o dataset FAFB contém uma correspondência espacial completa para todos os neurónios escolhidos.
- Não determina sinais ou pesos sinápticos fisiológicos completos.
- Não demonstra aprendizagem, inteligência geral ou reconstrução funcional integral do cérebro.
- Não significa que os IDs individuais já foram extraídos ou que os dados já foram descarregados.

## 7. Critérios de saída da Fase 2

**Concluído documentalmente:** dataset/snapshot selecionado; circuito piloto definido por tipos e arestas dirigidas; tarefa e condições de controlo definidas; baselines e métricas especificadas; fontes científicas e limitações registadas.

**Gate de dados ainda necessário antes de implementar o importador real:** obter acesso ao portal oficial, inspecionar metadados/cabeçalhos/tamanhos, confirmar os termos dos produtos concretos e materializar IDs e contagens reais. Este gate não requer usar o PC imediatamente se os produtos puderem ser inspecionados num ambiente remoto autorizado; não se deve contornar a autenticação.

A fase de seleção e desenho experimental só será considerada concluída depois de esse gate ser registado como aprovado ou bloqueado explicitamente por acesso. A implementação do motor de simulação não deve preceder a validação do esquema e da cobertura.
