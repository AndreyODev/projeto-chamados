# Sistema de Gestão de Chamados

## 1. Descrição do problema e do domínio

A empresa de suporte técnico atualmente controla as solicitações de clientes por meio de planilhas e mensagens dispersas. Essa prática dificulta a localização das solicitações, o acompanhamento do andamento dos atendimentos e a manutenção de um histórico básico e confiável dos chamados.

O sistema proposto pertence ao domínio de suporte técnico e tem como objetivo centralizar o registro, o acompanhamento e o histórico dos chamados, permitindo que pessoas clientes registrem e acompanhem suas solicitações e que pessoas atendentes consultem, atualizem e encerrem os chamados.

## 2. Objetivo da aplicação

A aplicação deverá centralizar o gerenciamento de chamados de suporte técnico, permitindo o registro das solicitações, o acompanhamento de seus status e a manutenção de um histórico básico das informações relacionadas aos atendimentos.

A primeira versão será planejada com baixa complexidade, priorizando as operações essenciais de registro, consulta, atualização de status e encerramento dos chamados.

## 3. Escopo inicial

A primeira versão do sistema contemplará as seguintes operações:

- Registro de chamados por pessoas clientes.
- Consulta dos chamados pelo cliente, limitada aos seus próprios chamados.
- Consulta dos chamados pela equipe de suporte.
- Visualização das informações dos chamados.
- Atualização do status pela pessoa atendente.
- Encerramento dos chamados pela pessoa atendente.

### 3.1 Fora do escopo inicial

Para manter a primeira versão simples e concentrada nas funcionalidades essenciais, não serão incluídos inicialmente:

- Serviço de notificações.
- Envio de mensagens por e-mail, SMS ou outros canais.
- Anexos de arquivos.
- Relatórios e dashboards.
- Sistema de prioridades ou SLA.
- Distribuição automática de chamados.
- Chat em tempo real.
- Avaliação do atendimento.

### 3.2 Evolução futura

Como evolução futura, poderá ser incorporado um **Serviço de Notificações**, responsável por informar a pessoa cliente sobre alterações relevantes no andamento do chamado.

Esse componente ficará fora do escopo da primeira versão.

## 4. Pessoas usuárias

| Pessoa usuária   | Objetivo principal                                   |
| ---------------- | ---------------------------------------------------- |
| Pessoa cliente   | Registrar e acompanhar seus próprios chamados.       |
| Pessoa atendente | Consultar, atualizar e encerrar chamados de suporte. |

### 4.1 Pessoa cliente

A pessoa cliente poderá:

- registrar um chamado;
- consultar seus próprios chamados;
- visualizar as informações de um chamado;
- acompanhar o status do chamado.

A pessoa cliente não poderá alterar o status nem encerrar um chamado.

### 4.2 Pessoa atendente

A pessoa atendente poderá:

- consultar os chamados;
- visualizar os detalhes dos chamados;
- alterar o status dos chamados;
- encerrar chamados quando o atendimento estiver resolvido.

Não será implementado, na primeira versão, um mecanismo de distribuição ou atribuição automática de chamados.

## 5. Requisitos funcionais

### RF01 - Registro de chamado

O sistema deve permitir que uma pessoa cliente registre um chamado informando, no mínimo, título e descrição.

### RF02 - Consulta de chamados pelo cliente

O sistema deve permitir que uma pessoa cliente consulte os chamados registrados por ela e acompanhe seus respectivos status.

### RF03 - Consulta de chamados pelo atendente

O sistema deve permitir que uma pessoa atendente consulte os chamados registrados no sistema e visualize suas informações.

### RF04 - Atualização de status

O sistema deve permitir que uma pessoa atendente altere o status de um chamado seguindo a sequência definida pela regra de negócio RN02.

### RF05 - Encerramento de chamado

O sistema deve permitir que uma pessoa atendente encerre um chamado quando a solicitação tiver sido resolvida.

## 6. Recursos principais do sistema

| Recurso   | Possíveis informações                                                                                               |
| --------- | ------------------------------------------------------------------------------------------------------------------- |
| Chamado   | identificador, título, descrição, status, data de abertura, cliente e atendente responsável pela última atualização |
| Cliente   | identificador, nome e contato                                                                                       |
| Atendente | identificador e nome                                                                                                |

Não serão definidos nesta etapa tabelas, tipos de dados ou comandos de banco de dados.

## 7. Regras de negócio iniciais

### RN01 - Status inicial

Todo chamado registrado deverá iniciar com o status **Aberto**.

### RN02 - Transição de status

Os status deverão seguir uma sequência simples:

**Aberto → Em andamento → Encerrado**

A primeira versão não permitirá pular etapas nem reabrir chamados encerrados.

### RN03 - Permissões do cliente

A pessoa cliente poderá consultar somente os chamados associados a ela.

### RN04 - Alteração de status

Somente uma pessoa atendente poderá alterar o status de um chamado.

### RN05 - Encerramento

Somente uma pessoa atendente poderá encerrar um chamado.

### RN06 - Registro da última atualização

O sistema deverá manter a identificação da pessoa atendente responsável pela última atualização do chamado, contribuindo para a manutenção de um histórico confiável dos chamados.

### RN07 - Data de abertura

A data de abertura do chamado deverá ser registrada automaticamente pelo sistema no momento de seu cadastro.

## 8. Fluxo prioritário - Registrar chamado

1. A pessoa cliente acessa a interface web e seleciona a opção de registrar um novo chamado.
2. A pessoa cliente informa os dados solicitados, como título e descrição.
3. A interface web envia os dados preenchidos para a API.
4. A API encaminha a solicitação para o back-end.
5. O back-end valida as informações recebidas e aplica as regras de negócio.
6. O back-end cria o chamado com status inicial **Aberto** e registra a data de abertura.
7. O registro do chamado é armazenado no banco de dados.
8. A aplicação retorna uma confirmação para a interface web, informando que o chamado foi registrado.

## 9. Decisões da equipe

- A primeira versão será mantida com baixa complexidade e concentrada nas quatro operações principais apresentadas no enunciado.
- O recurso Categoria foi retirado da primeira versão por não ser necessário para atender às funcionalidades obrigatórias.
- Não será implementado sistema de distribuição ou atribuição automática de chamados.
- Serão utilizados três status: Aberto, Em andamento e Encerrado.
- As transições de status serão sequenciais.
- Chamados encerrados não poderão ser reabertos na primeira versão.
- O atendente responsável pela última atualização será registrado para contribuir com a confiabilidade do histórico.
- O Serviço de Notificações será tratado como evolução futura e ficará fora do escopo inicial.

## 10. Em aberto

Poderá ser avaliada em uma evolução futura é se o histórico deverá armazenar apenas a última atualização realizada por uma pessoa atendente ou se deverá manter um registro completo de todas as alterações realizadas no chamado.

Para a primeira versão, será considerada apenas a identificação do atendente responsável pela última atualização, mantendo o escopo simples.

## 11. Organização inicial do repositório

A estrutura inicial do projeto foi organizada para separar a documentação das futuras camadas da aplicação:

```text
projeto-chamados/
├── README.md
├── docs/
│   ├── planejamento-semana-1.md
│   └── diagrama-arquitetura.md
├── frontend/
├── backend/
├── database/
└── prints/
```

A pasta `docs/` concentra os documentos de planejamento e arquitetura. As pastas `frontend/`, `backend/` e `database/` representam as futuras camadas da aplicação e permanecem sem implementação nesta etapa, pois a atividade não exige desenvolvimento de código ou criação do banco de dados.

A pasta `prints/` é utilizada para armazenar evidências visuais do desenvolvimento e organização do projeto.
