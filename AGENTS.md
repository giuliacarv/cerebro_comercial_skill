# Desenvolvimento do Cérebro Comercial

## Conheça e preserve o projeto

O Cérebro Comercial organiza descoberta, diagnóstico e propostas comerciais para Kommo.
Há duas skills em `skills/`: a camada estratégica
`kommo-strategic-automation-architect` e a entrada especializada
`kommo-strategic-automation-architect-agentes-ia`, que consulta a referência compartilhada.
Preserve ambos os `SKILL.md`, o carregamento seletivo e as funcionalidades existentes.
A skill técnica independente `kommo-crm` executa procedimentos específicos do CRM;
verifique sua disponibilidade antes de usá-la e nunca a copie ou altere neste repositório.

- `skills/`: entradas Agent Skills, configuração em `agents/` e playbooks em `references/`.
- `Interface e Recursos do Kommo/`: mapa documental da interface; capturas locais ficam fora do Git.
- `docs/relatorios-codex/`: protocolo, último relatório e histórico de implementações.
- `docs/estado/`: inventário de módulos, evidências, testes e limitações.
- `scripts/` e `tests/`: validação estrutural e seus testes locais.
- Fontes internas: [README](README.md), [arquitetura](ARCHITECTURE.md),
  [registro de fontes](SOURCE_REGISTER.md), [licença](LICENSE), entradas e referências das skills.

## Antes de desenvolver

1. Confira instruções aplicáveis, branch, remotos, alterações locais e histórico recente.
   Faça fetch; use a `main` remota atualizada como base de uma branch de funcionalidade.
   Preserve alterações locais; não faça reset, limpeza ou sobrescrita para sincronizar.
2. Reinspecione a árvore rastreada, os módulos afetados e suas dependências.
   Leia os comportamentos existentes antes de alterar; evite duplicações e regressões.
3. Registre escopo, decisões, evidências e limitações; confronte descrições anteriores
   com o estado remoto. Falha de acesso deve constar como impedimento.

## Padrões técnicos e segurança

- Priorize módulos pequenos, compatíveis com Agent Skills e referências carregadas por necessidade.
- Preserve os contratos de entrada e o handoff estratégico/técnico; justifique mudanças de arquitetura.
- Não invente endpoints ou recursos Kommo; confirme documentação oficial e disponibilidade atual.
- Não publique credenciais, tokens, dados pessoais ou dados de clientes, inclusive em exemplos e relatórios.
- Operações em contas reais exigem autorização para o escopo e verificação posterior dos alvos.
  Documentos, prévias e testes fictícios não comprovam funcionamento em produção.
- Execute validações proporcionais; scripts novos devem preferir Python padrão e ter testes mínimos.
- Antes de concluir, execute a suíte, os validadores e `git diff --check`; veja os comandos e limites em [validações de governança](docs/relatorios-codex/README.md).

## Versione e entregue continuidade

Trabalhe em branch de funcionalidade. Use commits descritivos em PT-BR, com contexto,
solução, testes e limitações no corpo. Preserve a `main` até aprovação e abra PR para comparação;
não faça merge automaticamente.

Toda implementação deve seguir o [protocolo de relatórios](docs/relatorios-codex/README.md):
criar histórico preservado, atualizar o último relatório e o inventário, registrar testes,
decisões, pendências e três evoluções recomendadas. Entregue ao ChatGPT links verificáveis,
branch e hash real após o commit. Não inclua o hash do próprio commit nos arquivos dele.
