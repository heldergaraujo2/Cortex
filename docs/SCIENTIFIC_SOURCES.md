# Fontes científicas e decisão inicial de dataset

**Atualizado:** 2026-10-28  
**Estado:** seleção para o primeiro protótipo decidida documentalmente; os arquivos de dados ainda não foram baixados nem inspecionados.

## 1. Decisão para o primeiro protótipo

**Dataset selecionado: FlyWire FAFB v783 (snapshot de outubro de 2023), representando o cérebro adulto feminino completo, incluindo os lobos ópticos e sem o cordão nervoso.** Esta escolha vale para o primeiro protótipo e para circuitos iniciais dentro do cérebro; não obriga o projeto a usar FAFB em todas as fases.

Motivos:
- O âmbito corresponde diretamente à primeira meta: trabalhar com um conectoma de cérebro, sem adicionar já o cordão nervoso.
- A versão tem documentação científica extensa e é utilizada em análises e modelos publicados.
- O guia oficial FlyWire identifica explicitamente o lançamento público FAFB v783 como CC BY-NC 4.0, permitindo planear a atribuição e o uso não comercial com clareza.
- O snapshot fixo melhora a reprodutibilidade face a depender apenas de uma base de dados viva.

**Alternativa para uma fase posterior: BANC v888**, que inclui cérebro e cordão nervoso e poderá ser mais adequado a circuitos sensório-motores integrados. A licença e os produtos concretos do BANC deverão ser confirmados no depósito antes de o importar.

Esta escolha não autoriza baixar o dataset completo. O primeiro download deve limitar-se aos produtos compactos necessários para inspecionar o esquema e selecionar um circuito pequeno, depois de verificar os metadados e a licença dos arquivos concretos.

## 2. Fontes primárias/oficiais

1. **Codex — catálogo e estatísticas de datasets:** https://codex.flywire.ai/  
   O catálogo consultado lista FAFB v783 (139.255 neurónios; 3.732.460 conexões de pares neuronais no contador do Codex) e BANC v888 (158.262 neurónios; 3.037.361 conexões de pares neuronais). Esses contadores não equivalem a número de sinapses individuais e podem depender do limiar de conexão adotado.

2. **FAQ oficial do Codex:** https://codex.flywire.ai/faq  
   Confirma versões disponíveis, snapshots estáticos, diferenças entre Codex e CAVE e recomenda downloads estáticos para análise em lote. A FAQ informa limiares padrão diferentes por dataset (FAFB: 5+ sinapses por par; BANC: 3+), portanto os contadores não devem ser comparados sem harmonizar filtros.

3. **Orientações oficiais de citação/licença FlyWire:** https://flywire.ai/guidelines  
   Declara que o lançamento público FAFB v783 está sob CC BY-NC 4.0. Verificar separadamente as condições aplicáveis ao BANC e aos arquivos concretos selecionados.

4. **Dorkenwald et al. (2024), “Neuronal wiring diagram of an adult brain”, Nature:** https://www.nature.com/articles/s41586-024-07558-y  
   Referência central para o conectoma FlyWire FAFB e seus limites.

5. **Lin et al. (2024), “Network statistics of the whole-brain connectome of Drosophila”, Nature:** https://www.nature.com/articles/s41586-024-07968-y  
   Explica filtros de qualidade e limiares usados para pares conectados; um par conectado não é o mesmo que uma sinapse individual.

6. **Bates et al. (2026), “Distributed control circuits across a brain-and-cord connectome”, Nature:** https://www.nature.com/articles/s41586-026-10735-w  
   Descreve o BANC, um connectoma de cérebro e cordão nervoso. O artigo identifica o BANC como um recurso vivo e indica depósitos estáticos para reprodutibilidade.

7. **Depósito de dados BANC:** https://doi.org/10.7910/DVN/7WTH1N  
   Verificar versão, metadados, licença e checksums dos arquivos antes de baixar.

8. **FlyConnectome:** https://github.com/seung-lab/FlyConnectome  
   Ferramentas e exemplos de acesso a dados de conectoma; não substitui a validação do esquema dos arquivos que serão efetivamente usados.

## 3. Comparação preliminar

| Critério | BANC v888 | FAFB v783 |
|---|---|---|
| Âmbito | Cérebro e cordão nervoso, fêmea adulta | Cérebro adulto, incluindo lobos ópticos; sem cordão nervoso |
| Snapshot observado | 20-05-2026 | Outubro de 2023 |
| Contagem no Codex consultado | 158.262 neurónios; 3.037.361 conexões | 139.255 neurónios; 3.732.460 conexões |
| Limiar padrão no Codex | 3+ sinapses por par | 5+ sinapses por par |
| Licença | Confirmar no depósito e nos arquivos selecionados antes de uso | Guia oficial FlyWire: CC BY-NC 4.0 |
| Utilidade provável | Fase posterior para circuitos cérebro–cordão | Primeiro protótipo de cérebro e comparação com literatura |
| Estado da decisão | Alternativa futura; licença dos arquivos concretos a confirmar | **Selecionado para o primeiro protótipo** |

Os números acima são contagens do catálogo, não uma garantia de que o arquivo de conexões escolhido tenha exatamente o mesmo número de linhas. Agregação por neuropilo, autapses, limiares e versão podem mudar a contagem.

## 4. Regras antes de importar

Para cada arquivo que vier a ser utilizado, registar no manifesto:
- dataset, snapshot e data de acesso;
- nome de produto/arquivo original e URL de origem;
- versão/commit do importador;
- tamanho em bytes e SHA-256;
- licença e citação aplicáveis;
- esquema, unidades, tipos de dados e semântica das colunas;
- filtros aplicados, incluindo limiar de sinapses e agregação por neuropilo;
- se o dado é medido, anotado, previsto, inferido ou derivado.

Não guardar datasets brutos grandes no Git. Manter manifesto, scripts e fixtures sintéticas pequenas rastreadas; dados brutos, caches, bases processadas e checkpoints ficam fora do repositório.

## 5. Limites científicos confirmados

- Um connectoma é uma representação estrutural de conectividade, não uma simulação funcional pronta.
- A conectividade dirigida descreve relações pré-sinápticas e pós-sinápticas; por si só não especifica completamente dinâmica, pesos fisiológicos, atrasos, estado inicial ou regras de plasticidade.
- Tipos de neurotransmissores podem incluir previsões e anotações verificadas; esses campos não são intercambiáveis.
- Uma conexão agregada por par neuronal não é uma sinapse individual.
- Um resultado de simulação não é uma gravação da atividade de uma mosca viva.

## 6. Estado e próximos critérios

**CONFIRMADO:** fontes oficiais consultadas documentam snapshots FAFB e BANC e recomendam downloads estáticos para análise em lote.  
**CONFIRMADO:** a orientação oficial FlyWire declara CC BY-NC 4.0 para o lançamento público FAFB v783 e o Codex documenta o snapshot e os contadores apresentados acima.  
**FORTEMENTE INDICADO:** FAFB v783 é a opção mais controlável para o primeiro protótipo centrado no cérebro, dada a documentação e a licença explícita.  
**HIPÓTESE:** a escolha de FAFB v783 reduzirá a complexidade inicial de integração face a começar por um dataset que também contém o cordão nervoso.  
**DESCONHECIDO:** o circuito inicial exato, a compatibilidade dos produtos de download com o importador ainda inexistente, o custo de simulação e o esquema efetivo dos arquivos ainda não descarregados.

A seleção final do primeiro circuito só será concluída após inspecionar os metadados reais, escolher uma tarefa testável e verificar que há dados suficientes para sustentar essa tarefa.
