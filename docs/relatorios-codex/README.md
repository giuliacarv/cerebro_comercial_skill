# Continuidade para o arquiteto ChatGPT

Ao encerrar uma implementação, registre o que foi entregue e as evidências que permitem
revisar e continuar o trabalho. Comece pelo [último relatório](ULTIMO_RELATORIO.md) e pelo
[inventário](../estado/ESTADO_DA_SKILL.json). As regras gerais estão em [AGENTS.md](../../AGENTS.md).

## Como concluir cada execução

1. Registre data com fuso, identificador da tarefa, objetivo, branch e hash da revisão base
   inspecionada. Informe também eventuais commits posteriores à base usados na implementação.
2. Crie `historico/AAAA-MM-DD-assunto.md`. Se o nome já existir, acrescente hora ou identificador;
   nunca substitua um relatório anterior. Correções posteriores devem ser um novo registro vinculado.
3. Use as dez seções abaixo. Vincule arquivos, fontes e evidências com caminhos relativos.
   Para testes, registre comando, ambiente, resultado observado e escopo não coberto.
4. Faça de `ULTIMO_RELATORIO.md` uma cópia integral do histórico mais recente, precedida de um
   link para o original. Adapte os links relativos à localização da cópia.
5. Atualize `docs/estado/ESTADO_DA_SKILL.json`, mantendo evidências e testes separados do status
   de implementação. Revise o inventário contra os arquivos reais, inclusive módulos novos/removidos.
6. Execute as validações abaixo e revise o diff. Faça commit e publique a branch e o PR quando
   autorizado. Apresente o hash real e a URL na entrega ao ChatGPT, após o commit;
   os arquivos desse commit registram apenas a revisão base, evitando autorreferência.
7. Na entrega, use a seção `RELATÓRIO PARA O ARQUITETO CHATGPT`: URL do PR, branch, commit,
   resumo, testes, links dos relatórios, problemas e próxima evolução. Se publicação falhar,
   descreva o impedimento e os comandos necessários para retomar, sem declarar publicação concluída.

O protocolo é executado pelo responsável por cada tarefa. Não há geração automática nem
proteção de branch configurada por estes documentos. Copiar apenas `skills/` para instalação
não instala a governança de desenvolvimento, que pertence ao repositório.

## Estrutura obrigatória do relatório

1. Identificação da execução, branch e objetivo.
2. Diagnóstico inicial do repositório e diferenças frente à especificação.
3. Arquivos criados, alterados e removidos.
4. Funcionalidades efetivamente implementadas.
5. Decisões arquiteturais e justificativas.
6. Testes realizados, comandos e resultados observados.
7. Estado atual das capacidades da skill.
8. Riscos, limitações e débitos técnicos.
9. Pendências e dependências externas.
10. Exatamente três evoluções recomendadas, cada qual com prioridade e critérios de aceitação.

## Estados e contrato do inventário

O esquema `1.0.0` usa `versao_esquema`, `atualizado_em` (ISO 8601 com fuso),
`revisao_base` (hash Git completo), `modulos`, `testes`, `dependencias_externas`,
`limitacoes_conhecidas` e `proximas_evolucoes`. Cada módulo tem `id`, `caminho`,
`responsabilidade`, `status_implementacao`, `evidencias`, `testes` e `dependencias`.
Evidências identificam caminho relativo à raiz e observação verificável.
Os testes registram escopo, status e evidência. Cobertura refere-se ao escopo inspecionado;
não equivale a percentual de cobertura de comportamento ou execução em CRM.

| Estado | Significado e evidência exigida |
| --- | --- |
| `documentado` | Orientação ou capacidade descrita em arquivo; não há prova de execução do comportamento. |
| `parcial` | Parte do escopo foi implementada; declarar precisamente o que falta e a evidência da parte entregue. |
| `implementado` | Artefato ou mecanismo entregue e inspecionável; comportamento ainda depende de validação no ambiente indicado. |
| `validado` | Critérios explícitos passaram em teste identificado, com resultado, data e ambiente. Só vale para esse escopo. |
| `não_verificado` | Evidência insuficiente ou verificação não executada; declarar dependência ou motivo. |

Esses estados descrevem evidência, sem progressão automática. Um playbook pode estar
`documentado` e ter integridade estrutural `validado`, enquanto sua operação no Kommo fica
`não_verificado`. Nunca promova uma capacidade comercial a `validado` pela existência de
texto, JSON válido, prévia ou teste fictício. Validação operacional exige conta, autorização,
cenário, critérios e leitura posterior dos efeitos; evite publicar dados dessa conta.

## Validações locais

Na raiz, com Python 3 disponível, execute:

```powershell
python -m unittest discover -s tests -v
python scripts/validar_governanca.py
git diff --check
```

O sucesso é saída zero nos três comandos. O validador usa apenas a biblioteca padrão:
confere UTF-8, links Markdown locais explícitos e âncoras, entradas das skills, JSON,
cobertura dos caminhos de módulos e equivalência entre histórico e último relatório.
Ele não consulta URLs externas, não interpreta todo o dialeto Markdown nem chama o Kommo.
Revise manualmente links não reconhecidos pelo formato simples e mudanças de comportamento.

Antes do commit, revise somente os arquivos destinados à publicação, procurando credenciais,
dados pessoais, referências de clientes e exemplos com dados reais. Varreduras por padrões
são auxiliares; ausência de correspondências não garante ausência de segredos.
Confira `git diff --cached --check` após adicionar caminhos explícitos ao índice;
evite incluir insumos locais não rastreados com `git add .`.

## Consulta ao histórico

- [Tarefa 001 — governança e continuidade](historico/2026-10-22-governanca-continuidade.md).
- [Tarefa 002 — verificações automáticas nos PRs](historico/2026-10-22-ci-governanca.md).
- [Última execução](ULTIMO_RELATORIO.md).

## Verificações automáticas nos Pull Requests

O workflow [governanca.yml](../../.github/workflows/governanca.yml) executa os testes,
o validador e `git diff --check` sobre as alterações do PR em relação ao commit da branch
de destino. Usar apenas `git diff --check` após checkout não detectaria whitespace já commitado.
O job exibido no PR chama-se **Validar governança**.

Ele roda em abertura, atualização de commits, reabertura, liberação para revisão e edição
do PR, incluindo troca de base. Não há filtros de caminho ou branch: PRs sobre branches
dependentes também são verificados. Execuções antigas do mesmo PR são canceladas.
Conflitos de merge e políticas de aprovação de workflows de forks podem impedir a execução;
nesses casos, confira o status do PR antes de interpretar ausência de resultado como sucesso.

O ambiente é Ubuntu 24.04 com Python 3.13, sem pacotes Python adicionais. Actions oficiais
de checkout e setup-python estão fixadas por hash completo e devem ser revisadas ao atualizar.
A permissão do token automático é `contents: read`; ele não persiste no checkout.
Nenhum segredo de repositório ou credencial Kommo é usado, nem há chamada ao CRM.

Os testes de comando executam o validador real em repositórios temporários e comprovam
falha para link quebrado, inventário incompleto e relatório divergente, além de whitespace
em snapshots Git. Dados e alterações deliberadamente inválidos ficam apenas nos temporários.
Os resultados e logs ficam na aba Checks do PR e no GitHub Actions.
As cópias usam `git ls-files`: ao desenvolver com arquivos novos, adicione seus caminhos
explicitamente ao índice antes de executar a suíte, para que também façam parte do cenário.

Uma execução vermelha sinaliza reprovação. Impedir tecnicamente o merge exige configurar
**Validar governança** como verificação obrigatória nas regras da branch; este workflow não
altera essas regras. Antes de exigir o check, ele deve estar incorporado à branch de destino
e ter uma execução observada. O PR da Tarefa 002 depende do PR de governança #2.

Referências oficiais consultadas em 2026-10-22:
[eventos pull_request](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request),
[checkout](https://github.com/actions/checkout) e [setup-python](https://github.com/actions/setup-python).
