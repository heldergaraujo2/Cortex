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
- a frente percorre um bin inteiro da projeção p, q ou v por passo; bins sem L1 mantêm-se como frames vazios, sem comprimir lacunas;
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


### Progressão uniforme da frente

A implementação preserva bins de projeção vazios entre o mínimo e o máximo observados. Assim, uma lacuna na malha não é removida para acelerar artificialmente a frente. O passo é uma unidade inteira da projeção da malha, não um intervalo de tempo biológico nem uma distância física calibrada.


## Resultado real final — execução corrigida no GitHub Actions

**FAFB v783 Data Validation #71:** sucesso no commit `784f30d43811da795fbda5ddadcbb5599ef91a8c`. O artefato inclui relatórios de validação, manifesto, baseline ME_L/ME_R e diagnósticos espaço-temporais ME_L/ME_R. https://github.com/heldergaraujo2/Cortex/actions/runs/41945748140

**Cortex CI #109:** 61 testes aprovados em cada versão Python 3.11, 3.12 e 3.13. https://github.com/heldergaraujo2/Cortex/actions/runs/41945747960

### Cobertura e população medida

- A tabela real tem 45.528 linhas e 45.528 root IDs únicos; SHA-256 `bdf4ce7f62cc63493d53eefad3816ff2dfd08b190e97b35a492e0e453df2f0f6`.
- 10.637/11.355 IDs do piloto têm atribuição; 718 permanecem sem atribuição.
- Cobertura L1 global: 1.572/1.775 = 88,56%. No experimento: 783 L1 atribuídos no hemisfério left e 789 no right. Não se calcula cobertura específica por lado para L1 sem atribuição, pois o lado desses IDs é desconhecido nesta tabela.
- Readout T4 limitado ao hemisfério estimulado: 2.986 células left (T4a 713, T4b 750, T4c 775, T4d 748) e 2.999 right (T4a 728, T4b 743, T4c 778, T4d 750).

### Resposta por eixo da malha medular

| Hemisfério | Eixo | Assimetria integrada entre +/− | Pico T4 + | Pico T4 − |
|---|---|---:|---:|---:|
| left / ME_L | p | 0,8359% | 0,021546 | 0,021539 |
| left / ME_L | q | 0,2204% | 0,023776 | 0,023733 |
| left / ME_L | v | 0,5120% | 0,021716 | 0,021793 |
| right / ME_R | p | 0,9783% | 0,021803 | 0,021872 |
| right / ME_R | q | 0,0440% | 0,023590 | 0,023540 |
| right / ME_R | v | 0,4656% | 0,021751 | 0,021654 |

Controles:
- Sem estímulo: pico T4 = 0 em todos os cenários.
- Flash ON global: atividade T4 integrada 0,995097 (ME_L) e 0,993021 (ME_R).
- Frentes opostas: cada L1 atribuído é ativado uma vez; direções opostas são reversões exatas, com energia e duração iguais.
- Bins inteiros de projeção vazios são mantidos; não há compressão de lacunas.

### Interpretação

**CONFIRMADO:** os estímulos sintéticos espaço-temporais são gerados a partir da malha p/q medular real, os dois sentidos são comparáveis em energia, o controlo sem estímulo permanece em zero e a resposta T4 é determinística.

**OBSERVAÇÃO DO MODELO:** a assimetria integrada entre sentidos opostos ficou entre 0,044% e 0,978%, ou seja, muito pequena nesta implementação.

**NÃO DEMONSTRADO:** seletividade direcional biológica. O índice é apenas assimetria computacional; não é DSI. O circuito ainda não inclui Mi4/Mi9/C3/CT1, sinais inibitórios, atrasos fisiológicos, integração dendrítica não linear ou parâmetros calibrados. Também não converte direções medulares em direções do campo visual.

### Estado do gate

A preparação no repositório e a validação no GitHub estão concluídas. O próximo gate é a primeira execução no PC Windows, usando `scripts/run_first_pc_validation.ps1`. A Fase 6 só será encerrada depois de comparar os resultados locais com estes relatórios da CI.
