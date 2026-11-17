# Cortex Programador — direção estratégica (17/11/2026)

## Missão
Construir um agente de programação autônomo para software, jogos, Blender, Unreal e Roblox, com memória persistente, aprendizagem baseada em evidência e propostas de autoaperfeiçoamento. **Ambição**: aproximar resultados práticos de assistentes de programação avançados em benchmarks definidos. Não há promessa de equivalência ao Claude Code/Opus nem de independência de LLMs.

## Três etapas e critérios

1. **Programador funcional (protótipo):** `CodingAgent.propose` aceita um provedor injetado, como futuro adaptador Qwen 8B, e gera proposta de código. Não existe conexão Qwen nem execução real de ferramentas nesta entrega. Conclusão exige adaptador real, ambiente isolado e tarefas end-to-end.
2. **Aprendizagem com experiências (protótipo):** `ExperienceStore` persiste resultados JSON e reintroduz histórico limitado em prompts. Isso é memória e recuperação contextual, **não** treinamento dos pesos do cérebro neural. Conclusão exige recuperação relevante, métricas e melhoria em tarefas não vistas.
3. **Autoaperfeiçoamento (protótipo protegido):** `propose_improvement` gera proposta sem alterar o código vivo; `accept_improvement` exige testes aprovados, melhora de pontuação e aprovação humana. Conclusão exige sandbox, isolamento de branches, regressão, rollback, revisão e benchmarks cegos.

## Segurança e avaliação
- Nenhum comando, script, download, patch ou autoalteração é executado automaticamente por este módulo.
- Verificação é callback injetado: o integrador deve prover sandbox e limites de recursos antes de usar código gerado.
- Não conceder acesso irrestrito ao computador, credenciais ou repositório de produção ao agente.
- Medir taxa de tarefas resolvidas, regressões, tempo/custo, generalização e retenção em conjunto de testes separado do treino.
- Qwen 8B é apoio inicial opcional, não componente implementado aqui. Independência futura é hipótese a investigar.
- O trabalho biológico FAFB/T4 permanece válido e separado; não se afirma validação biológica.

## Como testar
`python -m pytest -q tests/test_coding_agent.py`

## Próximas integrações
Adaptador Qwen/Ollama; executor de testes em contêiner isolado; conectores Blender/Unreal/Roblox/OpenCode; benchmark com casos reais; política de revisão de patches e rollback.
