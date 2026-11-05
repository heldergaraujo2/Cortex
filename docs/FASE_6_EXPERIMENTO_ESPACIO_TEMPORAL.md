# Fase 6 — coordenadas de coluna e estímulos espaço-temporais

**Estado:** preparação do primeiro diagnóstico espacial na malha da medula. A execução real na CI e a inspeção dos artefatos são gates obrigatórios antes de encerrar esta fase. Ainda não é um modelo de visão biologicamente validado.

## 1. O que as fontes permitem afirmar

### Coordenadas p/q

A tabela `column_assignment.csv.gz` contém `root_id, hemisphere, type, column_id, x, y, p, q`. A literatura de FAFB descreve `p,q` como coordenadas inteiras da malha hexagonal de colunas da medula. No referencial da medula:
- +p aponta anterodorsal;
- +q aponta posterodorsal;
- +v aponta dorsal.

As projeções inteiras usadas para ordenar uma frente ao longo dos três eixos são:
- p: `2p - q`;
- q: `2q - p`;
- v: `p + q`.

Essas são coordenadas/projeções da malha para ordenar colunas; não são distâncias físicas calibradas. `x/y` permanecem preservados, mas não entram na simulação porque a semântica/unidade específica desses campos da tabela ainda não foi validada por uma fonte primária.

### Medula não é retina

O artigo de Seung (2024) explicita que a malha de omatídios da retina é esquerda-direita invertida em relação à malha da medula devido ao quiasma óptico; por exemplo, back-to-front na retina corresponde a front-to-back na malha da medula. Portanto, os estímulos desta fase são rotulados como direções **na malha da medula** (+p/−p, +q/−q, +v/−v), nunca como esquerda/direita/frente/trás do campo visual.

A conversão para coordenadas do olho exigiria uma correspondência omatídio-coluna e uma transformação geométrica própria. O trabalho de Zhao et al. (2025) mostra que o mapeamento não é uma simples orientação global: a geometria da superfície ocular e a posição no campo visual mudam a direção preferida local.

### T4 e direção preferida

T4a–T4d são quatro subtipos com orientação dendrítica distinta e direções preferidas relacionadas à sua anatomia. A literatura mostra que as direções preferidas variam ao longo do olho e que o pareamento de cada subtipo com uma direção cardinal só é uma aproximação adequada em regiões centrais. Nesta fase, os quatro subtipos serão medidos separadamente, mas nenhum será rotulado com uma direção preferida global.

A seletividade direcional exige, no mínimo, entradas espacialmente deslocadas, assimetria temporal e interação não linear. A baseline atual contém apenas L1, Mi1, Tm3 e T4, com pesos positivos e sem atrasos, inibição ou dinâmica de membrana. A literatura identifica também entradas relevantes como Mi4, Mi9, C3 e CT1. Logo, a experiência atual é apenas um diagnóstico de sensibilidade da implementação à ordem espacial de entrada.

## 2. Experimento de engenharia v1

Para cada neuropilo, executado separadamente:
- ME_L usa apenas atribuições do hemisfério `left`;
- ME_R usa apenas atribuições do hemisfério `right`;
- somente neurónios L1 presentes no grafo e com atribuição válida entram no estímulo;
- cada L1 atribuído é ativado exatamente uma vez por passagem;
- a frente percorre uma fatia da malha por passo, ordenada por projeção p, q ou v;
- a direção oposta é a mesma sequência de fatias em ordem inversa.

Por construção, as duas direções opostas têm exatamente o mesmo conjunto de neurónios, duração, número total de eventos de entrada e amplitude. A comparação não pode ser explicada por diferença na quantidade de estímulo.

### Controles

1. **Sem estímulo:** todos os passos vazios; resposta deve permanecer zero.
2. **Flash ON global:** todos os L1 atribuídos ativados juntos no primeiro passo, seguido de silêncio.
3. **Frentes móveis:** +p/−p, +q/−q, +v/−v.

### Métricas

- resposta média T4 por passo e por subtipo T4a–T4d;
- pico e passo do pico;
- atividade T4 integrada ao longo da execução;
- cobertura L1 atribuída versus L1 disponível no subgrafo;
- assimetria de resposta entre sequências invertidas.

O índice de assimetria é `abs(A+ - A-) / (A+ + A-)`, em que A é a atividade T4 integrada. **Não é um índice biológico de seletividade direcional (DSI)**. É apenas uma medida de diferença entre duas execuções da abstração atual.

## 3. Limites que bloqueiam inferências

- Não usar `x/y` como coordenadas retinianas, graus visuais ou distâncias sem uma fonte primária e validação.
- Não converter +p/+q/+v em direções do mundo ou do olho.
- Não inferir a direção preferida de T4a–T4d a partir do nome do subtipo.
- Não afirmar seletividade direcional a partir de assimetria neste modelo.
- Não interpretar `syn_count` como eficácia sináptica medida.
- Não interpretar predições de neurotransmissor isoladamente como sinal funcional de cada sinapse.
- Os 718 neurónios piloto sem atribuição colunar permanecem fora do estímulo espacial; não serão imputados.

## 4. Critérios de aceitação da preparação

1. Parser real de `column_assignment.csv.gz` continua a passar e o hash da fonte é reportado.
2. Nenhuma mistura entre hemisférios ou neuropilos.
3. Cada L1 atribuído aparece exatamente uma vez por sequência.
4. Sequências opostas são reversões exatas e têm energia de entrada idêntica.
5. Flash e ausência de estímulo são controles explícitos.
6. Execução determinística e testes unitários aprovados.
7. Relatórios JSON de ME_L e ME_R publicados e inspecionados.
8. Documentação não chama a assimetria de seletividade direcional.

## 5. Fontes

- Seung, H. S. (2024). *Predicting visual function by interpreting a neuronal wiring diagram*. Nature 634, 113–123. https://doi.org/10.1038/s41586-024-07953-5 — coordenadas p/q, eixos da malha da medula e inversão retina-medula.
- Zhao, A. et al. (2025). *Eye structure shapes neuron function in Drosophila motion vision*. Nature 646, 135–142. https://doi.org/10.1038/s41586-025-09276-5 — orientação dendrítica de T4, variação espacial das direções preferidas e mapeamento olho-medula.
- Borst, A., Haag, J. & Mauss, A. S. (2020). *How fly neurons compute the direction of visual motion*. J Comp Physiol A 206, 109–124. https://doi.org/10.1007/s00359-019-01375-9 — requisitos de deslocamento espacial, filtragem temporal e interação não linear.
- Salazar-Gatzimas et al. (2018). *The Emergence of Directional Selectivity in the Visual Motion Pathway of Drosophila*. Neuron 94, 168–182.e10. https://doi.org/10.1016/j.neuron.2017.03.010 — contribuições excitatórias e inibitórias em T4.

## 6. Gate seguinte

A Fase 6 só termina depois da CI e da inspeção dos dois relatórios reais. Se o diagnóstico espacial for estável, a fase seguinte deve ampliar o circuito com entradas de T4 que faltam (Mi4, Mi9, C3, CT1 e outras conforme fonte e cobertura), introduzir sinais e filtros temporais explicitamente documentados e validar o mecanismo antes de qualquer alegação de direção preferida. Os primeiros testes locais no PC só devem começar depois de esta preparação e os gates automatizados estarem concluídos.


## Revisão da primeira execução — população de leitura corrigida

A primeira execução CI que incluiu as frentes espaciais (run #56, commit `1ac921ee5e6a0cc021eecf2e24df1c54146455a8`) terminou tecnicamente com sucesso, mas a inspeção dos JSON encontrou um erro de escopo na métrica: a entrada L1 era limitada ao hemisfério estimulado, enquanto o readout T4 incluía os dois hemisférios. Além disso, o denominador de L1 usado como cobertura era o total bilateral, não uma contagem específica do hemisfério. Portanto, os valores de resposta/asimetria daquele artefato ficam **supersedidos** e não serão interpretados.

Correção aplicada:
- selecionar o readout apenas entre neurónios T4a–T4d com atribuição explícita ao mesmo hemisfério do neuropilo;
- validar que o tipo atribuído coincide com o tipo primário do grafo e rejeitar duplicatas;
- reportar a cobertura L1 global (ambos os hemisférios) separadamente do número de L1 atribuídos ao hemisfério;
- não publicar uma cobertura L1 específica por hemisfério, pois os L1 sem atribuição não têm hemisfério conhecido por esta tabela.

A nova execução CI deve validar esta correção antes de aceitar os resultados. Os relatórios do run #56 continuam úteis apenas para provar que os scripts executaram e que os controles/pares de entrada foram produzidos; seus valores de resposta não são resultados finais.
