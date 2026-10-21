# Mapa da interface e dos recursos do Kommo

## Agente de IA nativo e Salesbot

**Escopo:** 27 capturas desta pasta, feitas em 20/10/2026. O mapa descreve o recurso que cada imagem ilustra e distingue o que é observável na captura do que foi confirmado na documentação oficial do Kommo.

As imagens mostram configurações reais da conta, inclusive instruções internas e dados do CRM. Por isso, este documento resume os padrões sem reproduzir nomes de pessoas, clientes, textos de prompt ou outros dados da conta. Os arquivos PNG ficam locais e estão excluídos do Git por `.gitignore`.

As capturas são registros daquele momento. Elas não comprovam que uma opção continua ativa ou igual na conta. Antes de configurar, ativar ou concluir algo sobre o estado atual, confira o próprio Kommo e as permissões e limites do plano.

## Como pensar nos recursos

### Salesbot

O Salesbot é um fluxo visual de etapas predefinidas, ativado por um gatilho, como uma mensagem, evento ou etapa do pipeline. As etapas fazem o roteiro configurado, por exemplo enviar uma mensagem ou executar uma tarefa de CRM. Ele é apropriado quando a sequência deve ser previsível e controlada.

### Agente de IA nativo

O Agente de IA interpreta a mensagem do cliente com base na Persona, nas Fontes de conhecimento e nas condições configuradas em Ações. Uma ação segue a estrutura **Quando → Fazer → Mais**: identifica um contexto, executa operações permitidas e aplica orientações adicionais. Pode, conforme as opções disponíveis na conta, responder com fontes, pedir informação, preencher campos, gerenciar tags, criar tarefas, transferir a conversa ou iniciar um Salesbot.

Agente de IA e Salesbot são recursos diferentes. O agente pode iniciar um Salesbot; nesse caso, desenhe e confira os gatilhos, a ordem e os critérios de parada para evitar que dois fluxos disputem a mesma conversa. A documentação do Salesbot descreve execução ligada a uma conversa e limita a um Salesbot em funcionamento por conversa. Recursos e limites podem variar por plano e configuração.

### Outros recursos de IA mostrados

- **Respostas sugeridas por IA:** prepara uma resposta para a equipe revisar e inserir como rascunho. A pessoa confere e envia; a sugestão não é, por si só, uma mensagem enviada ao cliente.
- **Sugestões de tarefas da IA:** identifica compromissos ou ações na conversa e sugere uma tarefa para revisão. A tarefa só é criada depois da confirmação da pessoa.
- **Kommo Copilot:** assistente invocado pela equipe para obter ajuda sobre o Kommo, resumir leads, identificar perguntas sem resposta e sugerir dados de campos. É diferente do agente autônomo que conversa com o cliente. A documentação informa que o modo Analyst pode usar dados de todo o espaço de trabalho, independentemente das permissões individuais; valide a autorização antes de usá-lo.
- **Fontes de conhecimento:** guardam conteúdo de negócio que o agente e as respostas sugeridas podem consultar. Sem conteúdo relevante nas fontes, não se deve presumir que a IA sabe a resposta.
- **Campos e grupos:** organizam dados estruturados do CRM. Ações do agente podem preencher campos disponíveis; o nome, o tipo e a finalidade de cada campo precisam ser conferidos antes de configurar.

## Índice das capturas

| Arquivo | O que a captura mostra | Recurso e função |
| --- | --- | --- |
| `01-salesbots-lista-e-gatilhos.png` | Lista de Salesbots e coluna de gatilhos, com opções para criar ou importar bots. | Ponto de gestão dos bots e de seus gatilhos. Um gatilho inicia o fluxo quando a condição configurada ocorre. Use a tela do pipeline ou as configurações de comunicação para inspecionar o gatilho específico antes de mudar algo. |
| `02-agente-ia-persona-configuracao-e-preview.png` | Editor de Persona, campos de estilo e regras, com painel de teste do agente. | Define papel, tom, extensão e idioma das respostas, atraso antes de responder e diretrizes. O Preview serve para testar perguntas e revisar o comportamento durante a configuração. |
| `03-agentes-ia-lista-status-e-creditos.png` | Lista de agentes, estado de ativação, abas de agentes próprios e exploração, e indicador de créditos. | Área de criação e acompanhamento dos agentes. O indicador de créditos é contextual à conta capturada; não deve ser reutilizado como saldo atual. |
| `04-configuracoes-respostas-e-tarefas-ia.png` | Controles de Resposta sugerida por IA e Sugestões de tarefas da IA. | Liga ou desliga dois recursos de apoio à equipe. Consulte também os recortes 05 e 06 para ver o propósito de cada um. |
| `05-respostas-sugeridas-ia-recorte.png` | Recorte do controle de resposta sugerida e referência às fontes de conhecimento. | Produz uma sugestão baseada em mensagem e fontes disponíveis. A equipe revisa, edita e decide se envia. |
| `06-sugestoes-tarefas-ia-recorte.png` | Recorte do controle de sugestões de tarefas. | Analisa mensagens recebidas e enviadas para identificar ações que podem exigir uma tarefa. A sugestão deve ser revisada antes de criar a tarefa. |
| `07-agente-ia-persona-regras-e-preview.png` | Visão ampla da aba Persona e do Preview. | Referência visual do editor completo: identidade, personalidade, estilo de resposta, diretrizes e teste. O texto específico configurado na conta foi omitido deste mapa. |
| `08-agente-ia-acoes-configuradas.png` | Resumo de várias ações já configuradas, cada uma com Quando, Fazer e Mais. | Mostra como condições distintas podem levar a respostas, preenchimento de campos, tarefas ou transferência para uma pessoa. É um exemplo de configuração da conta, não uma recomendação universal de regras. |
| `09-agente-ia-editor-de-condicao-e-transferencia.png` | Formulário de ação com condição de intenção, transferência e campos opcionais de mensagem e contexto. | Configura uma transferência para atendimento humano e a mensagem/contexto associados. A opção de pedir permissão para transferir deve ser escolhida segundo o processo e o canal. |
| `10-agente-ia-condicoes-por-intencao-sentimento-e-dados.png` | Menu de condições Quando, como intenção, assunto, sentimento, informação fornecida e conteúdo da mensagem. | As condições classificam o contexto da conversa para selecionar uma ação. Também é possível definir condições próprias, conforme a interface e a disponibilidade atual. |
| `11-agente-ia-condicoes-por-ausencia-formato-e-horario.png` | Continuação do menu de condições, incluindo ausência de resposta, formato da mensagem e horário. | Permite criar regras para espera, tipo de conteúdo recebido ou janela de atendimento. Confira a disponibilidade no plano e no canal antes de depender de temporizadores ou formatos. |
| `12-agente-ia-logica-todas-ou-qualquer-condicao.png` | Controle para executar a ação quando qualquer condição ou todas as condições forem atendidas. | Define a lógica de combinação entre condições da mesma ação: **qualquer** funciona como OR; **todas** funciona como AND. Teste os limites para confirmar que a ação não dispara cedo demais nem fica impossível de disparar. |
| `13-agente-ia-acoes-transferir-responder-ou-criar-tarefa.png` | Menu de Fazer com alternativas como transferir, não responder, repetir uma resposta, responder com informação específica ou adicionar tarefa. | Catálogo de operações de conversa e acompanhamento. A escolha afeta o que o agente fará automaticamente quando a condição ocorrer. |
| `14-agente-ia-acoes-fontes-campos-e-tags.png` | Menu de Fazer com uso de fonte de conhecimento, solicitação ao cliente, instruções de resposta, definição de campo e tags. | Permite responder com conteúdo aprovado, coletar informação e registrar ou categorizar dados no CRM. Verifique se a fonte está correta e se o campo/tag existe e tem o significado esperado. |
| `15-agente-ia-acoes-calendario-salesbot-etapa.png` | Menu de Fazer com tags, agendamento, início de Salesbot, mudança de etapa, alteração de responsável e envio de arquivo. | Ações capazes de acionar outros componentes do CRM. Algumas opções aparecem marcadas como dependentes de plano na captura; valide o plano e as consequências antes de usar. |
| `16-recorte-minimo-sem-conteudo-util.png` | Recorte muito pequeno, sem texto ou controle identificável. | Não permite atribuir uma função com confiança. Mantido e nomeado para preservar a captura; substitua por uma imagem mais completa se ela for necessária como evidência. |
| `17-agente-ia-regras-adicionais-e-contexto.png` | Cartões de ação e respectivas instruções adicionais em Mais. | O campo Mais complementa a ação com contexto, limites e orientações. Ele não substitui uma condição Quando nem uma operação Fazer. |
| `18-agente-ia-sentimento-handoff-campos-e-tarefa.png` | Exemplo de regra baseada em sentimento, com transferência, atualização de campos e criação de tarefa. | Demonstra uma resposta de escalonamento coordenada com registro interno. Na prática, defina responsável, prazo e tratamento de duplicidade de tarefa. |
| `19-agente-ia-captura-endereco-e-uso-de-fontes.png` | Exemplo de captura de endereço em campos estruturados e resposta com uma fonte selecionada. | Separa duas operações: registrar informação fornecida pelo cliente e responder com conteúdo de referência. A fonte e o mapeamento dos campos precisam ser conferidos. |
| `20-agente-ia-transferencia-e-criacao-de-tarefa.png` | Exemplo de consulta sobre serviço em andamento com transferência, resumo de conversa e tarefa. | Registra a demanda, encaminha para uma pessoa e cria acompanhamento. O resumo deve distinguir informação confirmada de informação ausente. |
| `21-agente-ia-atualizacao-de-campos-e-anexos.png` | Ações para classificar uma demanda, atualizar campos e reagir a mensagens com arquivo ou imagem. | Exemplo de captura de dados e registro de documentos recebidos ou pendentes. Defina se o agente pode sobrescrever um valor existente e como tratar anexos ambíguos. |
| `22-agente-ia-condicoes-e-captura-de-dados.png` | Regras distintas para capturar informações e lidar com perguntas específicas. | Mostra que cada cartão pode ter uma condição e um conjunto próprio de operações e instruções. O conteúdo particular das regras foi omitido. |
| `23-agente-ia-captura-do-nome-informado.png` | Condição de fornecimento de nome e preenchimento de um campo do lead. | Captura e registra o nome declarado durante a conversa. Se a pessoa falar em nome de outra, configure a distinção entre interlocutor e titular, sem inferir dados ausentes. |
| `24-agente-ia-condicao-intencao-e-handoff.png` | Regras para pedido de agendamento ou atendimento humano, com transferência e tarefa; outra regra registra o nome. | Combina reconhecimento de intenção com encaminhamento e acompanhamento. Não marque reunião nem confirme disponibilidade se a ação não consultar uma agenda válida. |
| `25-agente-ia-resumo-conversacional-em-campo.png` | Ação que espera informação suficiente na conversa e preenche um campo do lead com um resumo interno. | Exemplo de síntese de conversa gravada no CRM. Defina o objetivo do resumo, evidências permitidas, tamanho e o que fazer quando as informações forem insuficientes ou contraditórias. |
| `26-fontes-de-conhecimento-lista-e-uso.png` | Lista de fontes com tipo, idioma, número de subseções, uso, data de atualização e recursos que as utilizam. | Área de gestão e monitoramento das fontes. Ajuda a conferir atualização e vínculo com recursos de IA; nomes, responsáveis e métricas visíveis na imagem são dados da conta e não foram reproduzidos. |
| `27-configuracoes-copilot-respostas-e-tarefas-ia.png` | Configurações de IA com Copilot, Resposta sugerida e Sugestões de tarefas; o Copilot aparece habilitado na captura. | Reúne recursos distintos do Kommo AI. O Copilot apoia o trabalho da equipe; resposta e tarefa sugeridas dependem de revisão humana; o agente nativo é que pode conduzir conversas automaticamente. A captura não comprova o estado atual. |

## Limites e cuidados de configuração

1. Separe **Salesbot** de **Agente de IA** na análise: gatilhos e etapas determinísticas não são a mesma coisa que interpretações de linguagem natural.
2. Mantenha a IA apoiada em fontes aprovadas. Não trate o modelo como fonte de preço, prazo, elegibilidade ou política que não esteja documentada.
3. Use campos, tags, responsáveis e etapas existentes. Confirme entidade e significado antes de configurar gravações no CRM.
4. Reveja transferência para humano, encerramento de conversa, início de Salesbot, tarefas e agendamentos como efeitos operacionais. Use Preview ou homologação com casos controlados antes de ativar.
5. Faça leitura posterior da configuração e dos registros gerados. Um clique em Salvar não prova que a automação executou o fluxo esperado.
6. Confirme plano, canal, pipeline, permissões e limites atuais na conta. A lista de opções e regras pode mudar.

## Documentação oficial consultada em 20/10/2026

- [Visão geral do Agente de IA Kommo](https://support.kommo.com/docs/kommo-ai-agent): papel de Persona, Fontes, Ações, Integrações, Painel e mensagens de voz.
- [Configurar Agentes de IA](https://support.kommo.com/docs/ai-agent-manual-setup): criação, canais e etapas, limites documentados de ações e condições, opções de condição, Persona e integrações.
- [Adicionar e gerenciar fontes de conhecimento](https://support.kommo.com/docs/add-and-manage-ai-knowledge-sources): fontes usadas pelo agente e pelas respostas sugeridas.
- [Criar um Salesbot](https://support.kommo.com/docs/create-a-salesbot-in-kommo): construtor visual, etapas, modelos e execução em conversas.
- [Configurar gatilhos do Salesbot](https://support.kommo.com/docs/configure-your-salesbot-triggers): eventos e condições que iniciam bots.
- [Usar respostas sugeridas por IA](https://support.kommo.com/docs/work-with-ai-suggestions): sugestões como rascunhos revisáveis pela equipe.
- [Usar sugestões de tarefas](https://support.kommo.com/docs/task-suggestions): detecção de ações em mensagens e criação de tarefas após revisão.
- [Visão geral do Kommo AI](https://support.kommo.com/docs/kommo-ai-overview): distinção entre agente, Copilot, respostas sugeridas e tarefas sugeridas.
- [Usar o Kommo Copilot para gerenciar informações do lead](https://support.kommo.com/docs/copilot-ai-use): modos do Copilot, resumo e sugestões de campos; inclui a observação de permissões do modo Analyst.
