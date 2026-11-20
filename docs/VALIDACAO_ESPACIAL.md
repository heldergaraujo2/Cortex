# Validação espacial e de colunas visuais — FAFB v783

## Objetivo

A Fase 4 prepara a validação da relação entre o subgrafo estrutural L1/Mi1/Tm3/T4 e a tabela oficial `column_assignment.csv.gz`. O código não constrói ainda uma retina, não simula movimento e não interpreta a cobertura como prova de seletividade direcional.

## Fonte e estrutura esperada

A exportação pública FAFB v783 do FlyWire Codex inclui a tabela `column_assignment.csv.gz`. A estrutura documentada por inspeções independentes do produto é:

`root_id, hemisphere, type, column_id, x, y, p, q`

A validação no Cortex exige todos estes campos, mantém IDs como texto, valida `p/q` como inteiros e `x/y` como números finitos, calcula SHA-256 e preserva cada linha original em memória. Não exige unicidade de `root_id`, porque a unicidade por linha precisa ser verificada contra a exportação real, não presumida pelo código.

Fontes de referência:
- [FlyWire Codex — FAQ sobre o snapshot FAFB v783 e o sistema de coordenadas](https://codex.flywire.ai/faq?dataset=fafb)
- [FlyWire — orientações oficiais de citação e licença](https://join.flywire.ai/guidelines)
- [Documentação de formato e coordenadas das exportações FAFB v783](https://github.com/blendi-remade/streaming-fly-throughts/blob/main/docs/research/data-access.md) (referência secundária; confirmar sempre com o arquivo original antes de tratar um detalhe como medido).

## Implementação

- `cortex/spatial.py`: leitor estrito, SHA-256, cobertura por tipo primário, contagem de IDs sem correspondência, colunas por hemisfério e pares `(hemisphere, column_id)`.
- `scripts/inspect_fafb_columns.py`: gera JSON reproduzível com os resultados.
- `tests/test_spatial.py`: testa esquema, cobertura, hemisférios separados, valores inválidos, arquivo ausente e gzip corrompido.
- O workflow `FAFB v783 Data Validation` executa a inspeção real se o arquivo estiver presente e publica o relatório como artefato. Se estiver ausente, emite um aviso explícito; os testes sintéticos não substituem a inspeção real.

## Regras científicas

1. `column_id` é tratado como local ao hemisfério: a identidade da coluna é o par `(hemisphere, column_id)`, nunca o número isolado.
2. `x/y` e `p/q` são preservados em campos separados. O código não presume que sejam a mesma projeção, não aplica uma transformação retinotópica e não converte unidades sem evidência.
3. O FAQ do Codex descreve o visualizador FlyWire em voxels de 4 × 4 × 40 nm. Isso contextualiza as coordenadas do visualizador, mas não prova por si só as unidades/semântica dos campos `x/y` da tabela de colunas nem autoriza conversão automática.
4. A cobertura de `column_assignment` será medida contra os IDs/tipos primários reais de `consolidated_cell_types.csv.gz`. Ausência de atribuição não significa que o neurónio seja biologicamente inexistente ou não tenha função visual.
5. Os números reais de linhas, IDs, colunas, cobertura L1/Mi1/Tm3/T4a–T4d e SHA-256 só serão publicados após a presença e leitura bem-sucedida do arquivo original na branch.

## Estado do gate

**Resolvido em 2026-11-04:** `column_assignment.csv.gz` foi adicionado à branch e a inspeção real passou. Os números e o SHA-256 medidos estão registrados na seção seguinte. A Fase 4 está concluída no gate de ingestão/cobertura; a interpretação geométrica e a conversão para coordenadas visuais são gates distintos da Fase 6.


## Resultado da validação real — 2026-11-04

A execução FAFB v783 Data Validation #36 terminou com sucesso no commit `235e01bbb6360af977f8a0b2533ae2793340597e`. O artefato `fafb-v783-validation-report` contém `fafb_v783_column_assignment_report.json`.

- Arquivo: 462.838 bytes; SHA-256 `bdf4ce7f62cc63493d53eefad3816ff2dfd08b190e97b35a492e0e453df2f0f6`.
- 45.528 linhas; 45.528 root IDs únicos; zero IDs sem correspondência com a tabela de tipos primários.
- 1.581 pares únicos (hemisfério, column_id): 785 left e 796 right.
- IDs do piloto com atribuição: 10.637/11.355; sem atribuição: 718.
- Cobertura: L1 88,56%; Mi1 100%; Tm3 85,36%; T4a 98,90%; T4b 99,07%; T4c 90,82%; T4d 95,47%.

**Conclusão do gate de ingestão/cobertura:** aprovado. Isto não valida unidades, semântica física ou transformação retinotópica de x/y, nem prova seletividade direcional. A Fase 5 usa esta informação apenas como evidência de cobertura e mantém a dinâmica sem geometria visual.


## Interpretação da malha p/q — Fase 6

A literatura primária sobre FAFB descreve p/q como coordenadas discretas da malha hexagonal de colunas da **medula**. No referencial medular, +p é anterodorsal, +q posterodorsal e +v dorsal. As projeções para ordenar frentes são `2p-q`, `2q-p` e `p+q`, respectivamente (Seung, Nature 2024, https://doi.org/10.1038/s41586-024-07953-5).

A malha da retina é esquerda-direita invertida em relação à malha da medula pelo quiasma óptico. Portanto, o Cortex não rotula +p/−p/+q/−q/+v/−v como direções de movimento no campo visual. A transformação para o olho exige uma correspondência olho-medula e uma geometria que varia ao longo do campo visual (Zhao et al., Nature 2025, https://doi.org/10.1038/s41586-025-09276-5).

Os campos `x/y` continuam sem interpretação operacional. A implementação espacial da Fase 6 utiliza apenas `p/q` como índices da malha e mantém os hemisférios separados.
