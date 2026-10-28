# Contratos técnicos iniciais do Cortex

**Versão:** 0.1  
**Estado:** contratos de mensagens implementados em forma mínima; memória, coordenador e simulador ainda não implementados.

## 1. Limites

Estes contratos estabelecem interfaces entre componentes de software. Não representam uma teoria biológica nem provam que o sistema aprenda. As estruturas devem permanecer pequenas até o primeiro circuito e a tarefa experimental estarem definidos.

## 2. Identidade das instâncias

São definidos exatamente quatro identificadores estáveis:
- `C1`: coordenador;
- `C2`: perceção;
- `C3`: aprendizagem;
- `C4`: ação.

Cada instância deverá possuir estado dinâmico neural e parâmetros plásticos próprios. Não permitir que uma instância altere diretamente o estado interno de outra. A troca de informação ocorre por mensagens explícitas e pela memória coletiva.

## 3. Envelope de tarefa

A implementação inicial em `cortex.contracts.TaskEnvelope` contém:
- `task_id`: identificador obrigatório, não vazio;
- `task_type`: tipo de tarefa obrigatório;
- `payload`: dados da tarefa;
- `target_instance`: destino opcional entre C1–C4;
- `correlation_id`: identificador opcional para ligar mensagens relacionadas.

A estrutura é imutável no nível do objeto para reduzir mutações acidentais durante o encaminhamento. A imutabilidade é superficial: objetos mutáveis aninhados no payload ainda devem ser tratados como somente leitura pelo consumidor.

## 4. Resultado de cérebro

`cortex.contracts.BrainResult` contém:
- tarefa e instância de origem;
- saída estruturada;
- estado epistémico;
- confiança opcional no intervalo [0, 1];
- referências de proveniência;
- versão da memória coletiva lida, se aplicável.

Confiança numérica não é probabilidade calibrada automaticamente. Só deve ser interpretada como probabilidade depois de um procedimento de calibração demonstrado.

## 5. Estado epistémico

O enum inicial conserva as quatro categorias do projeto:
- `CONFIRMADO`;
- `FORTEMENTE_INDICADO`;
- `HIPOTESE`;
- `DESCONHECIDO`.

A categoria descreve a evidência associada à afirmação, não o nível de confiança subjetiva de uma instância.

## 6. Memória coletiva — contrato a implementar

A memória coletiva futura deve fornecer operações explícitas equivalentes a:
- leitura por chave/filtro e versão;
- escrita atómica com versão esperada;
- criação de nova revisão em vez de sobrescrita silenciosa;
- preservação de afirmações contraditórias e ligação a um grupo de conflito;
- proveniência obrigatória: instância, tarefa, fontes, timestamp lógico, versão e estado epistémico;
- operações determinísticas de teste para conflito e concorrência.

A implementação não deve escolher automaticamente uma versão como verdade só por ser mais recente ou por vir de C1. Resolução de conflitos deve ser explícita, auditável e manter o histórico.

## 7. Coordenador e orquestrador — contrato a implementar

C1 é uma das quatro instâncias e pode propor distribuição e síntese de tarefas. Um orquestrador determinístico separado deve validar mensagens, controlar timeouts, registar eventos e recuperar falhas. O orquestrador não é um quinto cérebro nem deve gerar as conclusões neurais usadas para medir o núcleo.

Resultados de C2–C4 devem permanecer consultáveis após a síntese de C1. Divergências não podem ser descartadas silenciosamente.

## 8. Motor de simulação — contrato a implementar

O futuro motor deve separar:
1. dados estruturais importados e sua proveniência;
2. modelo de dinâmica e parâmetros explícitos;
3. estado instantâneo de cada instância;
4. entradas experimentais e saídas observáveis;
5. plasticidade/aprendizagem;
6. configuração, sementes e registos de execução.

Parâmetros ausentes do dataset precisam de ser identificados como estimativas ou escolhas de engenharia. O motor deve permitir um circuito sintético minúsculo para testes unitários e um circuito biológico reduzido para validação posterior.

## 9. Regras de concorrência e reprodutibilidade

- IDs de tarefa e registos de memória são explícitos.
- Escritas concorrentes devem usar versão esperada/compare-and-swap ou transação equivalente.
- Sementes e configuração devem ser registadas em cada execução estocástica.
- Não partilhar silenciosamente pesos nem estados neurais entre instâncias.
- O mesmo fixture sintético e a mesma configuração devem produzir resultados determinísticos quando o backend assim o declarar.
- Timeout e falha de instância não devem corromper memória ou eliminar resultados de outras instâncias.

## 10. Critérios mínimos para expandir os contratos

Antes de implementar memória e coordenação completas, os testes devem cobrir:
- rejeição de IDs e campos obrigatórios inválidos;
- validação de confiança e versões;
- preservação de proveniência;
- ausência de mutação acidental de mensagens;
- escrita concorrente, conflito e histórico na memória;
- timeout e falha de uma instância;
- separação de estado entre duas instâncias;
- comportamento com quatro instâncias e baselines de uma instância.

Os testes atuais cobrem apenas os contratos de mensagem. Os restantes são critérios futuros, não funcionalidades já implementadas.
