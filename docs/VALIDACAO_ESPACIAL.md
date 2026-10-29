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

**Código e testes de unidade preparados; validação espacial real ainda não concluída.** Na branch `data/fafb-v783-inputs`, o arquivo `column_assignment.csv.gz` ainda não foi encontrado na última inspeção. Até ser adicionado, não é correto declarar a Fase 4 concluída nem começar a baseline espacial/dinâmica.
