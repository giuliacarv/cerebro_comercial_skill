# Tarefa 002 — Complementos de validação contínua

## 1. Identificação da execução, branch e objetivo

Execução: TAREFA-002-COMPLEMENTOS, em 2026-10-22, America/Sao_Paulo (UTC−03:00).
Branch: `feat/ci-validacao-governanca`. Objetivo: fechar lacunas da automação de qualidade
reaproveitando a CI e o validador da Tarefa 002, sem implementar capacidades comerciais.
Base remota inspecionada: `fe5fcc24da527a3edda57bba65d4813665654339` (`origin/main`).
Dependência explícita: `cd711dfa015c8d6537d06cb6ee60e41a399fc00e`, branch do PR #3,
que já contém a Tarefa 001 e a primeira versão da CI. Os PRs #2 e #3 continuam abertos;
nenhum merge foi feito na `main`. Esta branch deriva de `feat/ci-governanca` e o novo PR
será direcionado a essa base para manter a diferença incremental.

## 2. Diagnóstico inicial do repositório

O `fetch` confirmou `origin/main` em `fe5fcc2` e as branches remotas de governança e CI.
O PR #2 (governança) e o PR #3 (CI) estavam abertos, não integrados à `main`. O Actions
registrava sucesso no commit `cd711dfa015c8d6537d06cb6ee60e41a399fc00e` para a configuração
anterior. A main permaneceu intacta.

A inspeção encontrou duas entradas Agent Skills, 13 referências, configuração Codex, mapa
documental, validador estrutural, testes e workflow `governanca.yml`. A arquitetura estratégica,
a entrada especializada e a skill técnica externa `kommo-crm` estavam separadas como esperado.
O workflow anterior já verificava testes, links, inventário, relatórios e whitespace em PRs,
mas não tinha execução manual, escopo explícito para `main`, verificação de sintaxe Python ou
scanner local de segredos. O validador já suportava espaços, percent-encoding, fragmentos,
URLs externas sem rede e estados `não_verificado`; faltavam casos de teste para alguns desses
contratos, JSON inválido, caminho de módulo ausente e identificadores de execução divergentes.
Na revisão final, também foi fechada a lacuna de IDs de dependências do inventário: referências
desconhecidas e dependências repetidas dentro do mesmo módulo agora reprovam a validação.

As instruções, inventário e relatórios de continuidade foram consultados. `.agents/` e
`Insumos para Kommo/` estavam não rastreados e foram preservados. O trabalho em andamento da
evolução de roteamento foi isolado em stash e não foi incluído nesta branch.

A consulta à API de proteção da branch retornou HTTP 403 para a integração. A listagem pública
de rulesets retornou lista vazia; isso não prova ausência de proteção via outro endpoint.
Nenhuma regra administrativa foi alterada.

## 3. Arquivos criados, alterados e removidos

Criados:

- [Novo workflow para `main`](../../../.github/workflows/validar-governanca.yml), com PR para `main`,
  execução manual, validação Python e verificação de segredos evidentes.
- [Validador do diff](../../../scripts/validar_diff_pr.py), com AST e detecção limitada de segredos.
- [Testes do validador de diff](../../../tests/test_validar_diff_pr.py).
- Este relatório histórico; o [último relatório](../ULTIMO_RELATORIO.md) reproduz este conteúdo.

Alterados:

- [Workflow existente](../../../.github/workflows/governanca.yml), preservado para PRs entre
  branches dependentes e filtrado para não duplicar a execução em PRs para `main`.
- [Validador estrutural](../../../scripts/validar_governanca.py), com diagnóstico de JSON,
  tipos e caminhos, avisos informativos e comparação de identificadores de execução.
- [Testes de governança](../../../tests/test_validar_governanca.py) e [testes de CI](../../../tests/test_ci_governanca.py).
- [AGENTS.md](../../../AGENTS.md), [README](../../../README.md), [protocolo de relatórios](../README.md),
  [último relatório](../ULTIMO_RELATORIO.md) e [inventário](../../estado/ESTADO_DA_SKILL.json).

Removidos: nenhum. Os dois `SKILL.md`, as referências, a licença, a arquitetura,
as fontes e os históricos anteriores foram preservados. `kommo-crm` não foi copiada nem alterada.

## 4. Funcionalidades efetivamente implementadas

O novo workflow executa em Pull Requests com destino `main` e permite `workflow_dispatch`.
O workflow anterior permanece para PRs entre branches dependentes, sem disparar em PRs para `main`.
Mantém Ubuntu 24.04, Python 3.13, actions oficiais fixadas por SHA, permissão `contents: read`,
timeout de dez minutos, checkout sem credencial persistente e sem `pull_request_target`.
Executa `unittest`, validação de sintaxe Python em memória, verificação de padrões evidentes
de segredo em linhas adicionadas, validador estrutural e `git diff --check` contra a base.

O scanner não mostra valores, reconhece alguns formatos conhecidos e atribuições sensíveis,
ignora placeholders explícitos e não grava bytecode. O validador estrutural agora informa
arquivo/linha/coluna para JSON inválido, confere tipos dos campos do inventário e compara IDs
de execução disponíveis entre relatório histórico e último relatório. Confere referências de
dependências do módulo contra IDs existentes e acusa dependências duplicadas. Dependências externas
`não_verificado` permanecem aceitas e geram apenas aviso informativo.

Foram ampliados testes para links com espaços e codificação, URLs externas sem acesso de rede,
ausência de módulos/caminhos, JSON inválido, divergência de identificadores, estado Kommo
`não_verificado`, sintaxe Python e detecção de segredo sem exposição do valor.
Um teste adicional comprova falha para dependência com ID inexistente.

## 5. Decisões técnicas e justificativas

- Reutilizar `validar_governanca.py` e sua suíte reduz duplicação da lógica existente.
- A branch filha e o PR para `feat/ci-governanca` deixam visível somente o complemento e preservam
  a cadeia de dependência com os PRs #2 e #3, sem diff enganoso contra a `main` ainda não atualizada.
- `workflow_dispatch` usa `origin/main` como referência quando não há evento de PR; PRs para main
  usam o SHA fornecido pelo evento.
- `ast.parse` verifica sintaxe sem criar arquivos `.pyc` no checkout.
- O scanner próprio é deliberadamente restrito ao diff e a padrões evidentes; não foi apresentado
  como garantia de ausência de segredos nem como substituto de revisão.
- Não houve mudança nas skills comerciais ou operações Kommo. Sem autorização e acesso administrativo
  confirmado, regras da branch não foram modificadas.

## 6. Testes realizados e resultados observados

Ambiente local: Windows, PowerShell, Git e Python 3.13.14 do runtime Codex; somente biblioteca padrão.
Comandos executados contra a revisão base e o resultado observado:

| Verificação | Resultado |
| --- | --- |
| `python -m unittest discover -s tests -v` | 27 testes aprovados; inclui casos positivos e negativos em cópias temporárias. |
| `python scripts/validar_governanca.py` | Saída zero: 26 Markdown, 2 entradas e 20 módulos; JSON, inventário, links e relatório íntegros. Três avisos informativos de dependências `não_verificado`. |
| `python scripts/validar_diff_pr.py origin/main` | Saída zero: sintaxe Python alterada válida e nenhum segredo evidente no diff adicionado; valores não são exibidos. |
| `git diff --check origin/main` | Saída zero; sem erros de whitespace no diff. |
| GitHub Actions para branch dependente | Aprovado no [run 39782340769](https://github.com/giuliacarv/cerebro_comercial_skill/actions/runs/39782340769), no commit inicial `4a0e041e6dcbad290ef1c6766bee86335f74ed22`; testes, validação estrutural e whitespace concluíram com sucesso em `.github/workflows/governanca.yml`. |
| Novo workflow para PRs destinados à `main` | Não verificado; o run do PR #4 foi o workflow de branches dependentes e não executou a nova configuração `validar-governanca.yml` nem o scanner de diff. |
| Integração Kommo | Não executada; `não_verificado`. |

## 7. Estado atual das capacidades da skill

O inventário preserva as duas entradas, 13 referências e o mapa documental e acrescenta o
módulo de validação de diff. As capacidades comerciais continuam documentadas, sem alteração
ou promoção de status baseada na existência de arquivos. A CI e o scanner são mecanismos de
governança; seus testes estruturais não validam o runtime de Agent Skills ou operações reais.
Consulte o [inventário estruturado](../../estado/ESTADO_DA_SKILL.json) para evidências, dependências
e estados atualizados.

## 8. Riscos, limitações e débitos técnicos

- O scanner de segredos cobre padrões selecionados em linhas adicionadas, pode ter falsos positivos
  e não garante detecção completa; arquivos fora do diff não são examinados.
- O GitHub Actions aprovou o workflow de branches dependentes no PR #4, mas isso não executou
  `validar-governanca.yml` destinado à `main` nem o scanner de diff. A nova configuração continua
  `não_verificado` até haver execução em PR para main ou despacho manual observável.
- A leitura da proteção da `main` não foi autorizada para a integração. Regras obrigatórias continuam
  dependendo de decisão e configuração administrativa.
- Sem regra exigindo o status check, uma execução vermelha não bloqueia tecnicamente o merge.
- O validador Markdown é intencionalmente simples e não valida todos os dialetos ou comportamento.
- O repositório público ainda tem recomendação histórica de privacidade e termos proprietários;
  essa inconsistência permanece sem alteração de licença ou distribuição.

## 9. Pendências e dependências externas

Revisar este complemento no PR filho da `feat/ci-governanca`; depois da integração da cadeia,
observar uma execução da nova configuração em PR para `main` e, separadamente, um disparo manual.
Configurar proteção da branch somente após autorização administrativa explícita e conferir o nome
real do check. GitHub Actions, runners, Python 3 e Git são dependências. Nenhuma conta Kommo,
credencial CRM ou serviço externo de rede é usado pelos testes.

## 10. Três evoluções recomendadas

| Prioridade | Evolução | Critérios de aceitação |
| --- | --- | --- |
| P1 | Exigir o check de governança na proteção da main após integração | Regra exige PR e `Validar governança`; PR de teste comprova bloqueio em execução vermelha; bypass fica documentado. |
| P2 | Ampliar cenários fictícios de regressão do roteamento seletivo | IA, Salesbot, RevOps, operação técnica, ambiguidade, carregamento mínimo e autorização têm expectativas verificáveis sem runtime/CRM. |
| P3 | Definir homologação operacional autorizada em ambiente isolado | Escopo, conta, dados fictícios, autorização, reversão e critérios de leitura posterior são definidos antes de qualquer execução real. |
