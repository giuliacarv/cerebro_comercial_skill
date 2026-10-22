# Tarefa 002 — Evidência de validação remota da CI

## 1. Identificação da execução, branch e objetivo

Execução: TAREFA-002-VALIDACAO, em 2026-10-22, America/Sao_Paulo (UTC−03:00).
Branch: `feat/ci-governanca`. Objetivo: automatizar testes, integridade e diff em Pull Requests.
Base remota inspecionada: `fe5fcc24da527a3edda57bba65d4813665654339` (`origin/main`).
Dependência explícita: `607b7f16e66b569fb46cafc3869baba06bad1f31`, do PR #2 de governança,
ainda não incorporado à main no início desta execução. A branch foi criada da main atualizada
e avançada por fast-forward até essa dependência. Nenhum merge foi feito na main.
O PR desta evolução compara com `feat/governanca-relatorios-codex`, isolando a revisão de CI.
Implementação publicada em `9b1e08fc02922f0301b03973a4482dcbe2e3d836`,
[PR #3](https://github.com/giuliacarv/cerebro_comercial_skill/pull/3). Este segundo registro preserva
o [snapshot anterior à publicação](../historico/2026-10-22-ci-governanca.md) e acrescenta evidência observada.
O hash deste registro documental será entregue após o commit, sem autorreferência.

## 2. Diagnóstico inicial do repositório

Fetch confirmou main em `fe5fcc2` e governança em `607b7f1`. Os arquivos rastreados estavam
sem alterações locais. `.agents/` e `Insumos para Kommo/` continuavam não rastreados e foram preservados.
Foram reinspecionados árvore remota, histórico, AGENTS, protocolo, inventário, validador e testes.
O projeto tinha sete testes locais, mas nenhum workflow ou check automático de PR.

A inspeção identificou que `git diff --check` sem revisões não examina alterações já commitadas
em checkout limpo. A CI deve comparar o commit da base do evento com o checkout do PR.
O validador existente já rejeita links, inventário e relatórios inconsistentes; a evolução
reutiliza esse comando e comprova seus códigos de saída com repositórios temporários.

## 3. Arquivos criados, alterados e removidos

Criados:

- [Workflow](../../../.github/workflows/governanca.yml).
- [Testes de comando](../../../tests/test_ci_governanca.py).
- Este histórico: `docs/relatorios-codex/historico/2026-10-22-ci-governanca.md`.

Alterados:

- [Protocolo](../README.md), com execução automática, limites e consulta ao histórico.
- [Último relatório](../ULTIMO_RELATORIO.md), atualizado para esta execução.
- [Inventário](../../estado/ESTADO_DA_SKILL.json), com módulo de CI e três próximas evoluções.

Neste fechamento adicional, foram atualizados inventário e último relatório e criado este
registro `2026-10-22-ci-governanca-validacao.md`. O relatório inicial da Tarefa 002 foi preservado.
Nenhum arquivo removido. O histórico da Tarefa 001, os dois SKILL.md, as 13 referências,
o YAML da skill, mapa, arquitetura, fontes, licença e README da raiz foram preservados.

## 4. Funcionalidades efetivamente implementadas

Workflow `Governança`, job `Validar governança`, em todos os PRs, sem filtros de caminho ou base.
Eventos: abertura, novos commits, reabertura, liberação de rascunho e edição, incluindo troca de base.
Execuções antigas do mesmo PR são canceladas. Ubuntu 24.04 e Python 3.13, limite de dez minutos.
Checkout com histórico completo e sem credencial persistida; token automático somente de leitura.
Actions oficiais checkout/setup-python v6 fixadas por hashes completos consultados no upstream.

Passos: `python -m unittest discover -s tests -v`, `python scripts/validar_governanca.py`
e `git diff --check "$BASE_SHA" HEAD`, usando a revisão base do evento por variável de ambiente.
Não há dependências Python adicionais, segredos configurados, credenciais Kommo nem chamadas ao CRM.

Cinco testes de comando usam cópias temporárias: repositório válido passa; link quebrado,
inventário incompleto, relatório divergente e whitespace no diff falham.
As falhas são deliberadas e isoladas em temporários, tanto localmente quanto no runner;
não são publicadas como alterações inválidas.

## 5. Decisões arquiteturais e justificativas

- Reutilizar comandos locais evita duplicar regras de validação dentro do workflow.
- Executar o código do evento `pull_request` com leitura mínima mantém o teste no contexto do PR.
- Fixar actions por SHA permite identificar exatamente o código externo executado.
- Comparar snapshots Git cobre whitespace commitado; verificar apenas a árvore limpa não cobriria isso.
- Testar o processo real e seu exit code comprova que a CI recebe reprovação para os três defeitos exigidos.
- PR dependente permite revisão isolada enquanto o PR #2 aguarda aprovação, preservando a main.
- Regras administrativas de merge não são alteradas: o workflow publica o resultado; exigir o check
  é uma evolução explícita e depende da incorporação dos PRs e da decisão do responsável.

## 6. Testes realizados e resultados observados

Ambiente local: Windows, Git e Python 3.13.14 do runtime Codex, biblioteca padrão.
O alias Python do WindowsApps apresentou erro de caminho; a execução foi retomada com o
interpretador Python fornecido pelo runtime, sem alterar a instalação do sistema.
Na primeira montagem de cenário, dois destinos novos ainda não estavam no índice e foram
corretamente apontados como ausentes na cópia temporária. Após inclusão explícita dos arquivos,
os 12 testes passaram. Essa exigência de preparação está documentada no protocolo.

| Verificação | Resultado |
| --- | --- |
| Testes unitários e de comando | `python -m unittest discover -s tests -v`: 12 testes aprovados, incluindo os cinco cenários reais de processo/diff. |
| Validador de governança | `python scripts/validar_governanca.py`: 25 Markdown, duas entradas, 19 módulos; saída zero. |
| Diff e preservação das skills | `git diff --check`, `git diff --cached --check` e comparação com a dependência: sem erro de whitespace; skills, histórico anterior e documentos originais sem alterações. |
| Revisão de segredos/dados pessoais | Revisão dos seis arquivos do diff e varredura por padrões de credenciais, JWT, chaves privadas, e-mails, CPF e telefone sem ocorrências. |
| GitHub Actions | [Execução 39777854814](https://github.com/giuliacarv/cerebro_comercial_skill/actions/runs/39777854814): concluída com success, evento pull_request, commit `9b1e08fc02922f0301b03973a4482dcbe2e3d836`. Todos os passos do job Validar governança aprovados no Ubuntu. Essa execução inspecionou 24 Markdown; este novo registro eleva o conjunto local a 25. |
| Integração Kommo | Não executada; não_verificado. |

## 7. Estado atual das capacidades da skill

O inventário passa a 19 módulos: os 18 anteriores e o workflow de CI.
Os 16 componentes de orientação permanecem documentados; configuração Codex, governança
e workflow são implementados, com testes e limites explicitados separadamente.
Nenhuma capacidade comercial ou operacional em conta CRM foi adicionada ou validada.
O novo workflow só estará disponível na main após aprovação e incorporação dos PRs.

## 8. Riscos, limitações e débitos técnicos

Check reprovado não impede merge sem configuração de verificação obrigatória na branch.
Políticas de forks, Actions desabilitado, indisponibilidade de runner ou conflito de merge podem
impedir execução; ausência de resultado não é sucesso. O validador continua limitado a Markdown
explícito simples e não substitui revisão de comportamento ou scanner de segredos.
As versões das actions e do Python exigem manutenção; nenhuma atualização automática foi configurada.
A inconsistência de visibilidade pública versus orientação antiga de privacidade permanece registrada
na Tarefa 001. Licença e distribuição continuam preservadas.

## 9. Pendências e dependências externas

Aprovar primeiro o PR #2; depois ajustar a base do PR de CI para main e incorporar por revisão.
Nenhum merge automático está autorizado pelo protocolo. A primeira execução foi observada com sucesso e está vinculada neste registro.
O novo commit apenas documental será revalidado pela mesma CI; sua evidência será entregue ao final.
Runner GitHub, actions oficiais e acesso para publicar são dependências externas.
Insumos não rastreados continuam fora da publicação. Não há dependência de conta Kommo nesta tarefa.

## 10. Três evoluções recomendadas

| Prioridade | Evolução | Critérios de aceitação |
| --- | --- | --- |
| P1 | Criar cenários fictícios de regressão do roteamento seletivo | IA, Salesbot, RevOps e operação técnica com rotas esperadas revisadas; casos negativos de ambiguidade, carregamento mínimo e autorização; sem CRM. |
| P2 | Tornar o check obrigatório após incorporação dos PRs | Aprovação administrativa; branch exige Validar governança; execução vermelha impede merge; regras e limites de bypass documentados. |
| P3 | Definir homologação operacional autorizada em ambiente isolado | Conta, escopo, responsável, dados fictícios, autorização e reversão definidos; persistência, silêncio, duplicidade e handoff validados só por efeitos observados. |
