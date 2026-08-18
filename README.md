# Projeto Chamados

Sistema web de gestão de chamados para uma empresa de suporte técnico.

## Objetivo

Planejar uma aplicação web capaz de centralizar o registro, acompanhamento, atualização e encerramento de chamados de suporte, substituindo o controle realizado por planilhas e mensagens dispersas.

## Escopo inicial

A primeira versão do sistema será planejada para permitir:

- Registro de chamados por pessoas clientes;
- Consulta dos próprios chamados pela pessoa cliente;
- Consulta dos chamados pela pessoa atendente;
- Visualização das informações dos chamados;
- Atualização do status dos chamados;
- Encerramento dos chamados.

## Pessoas usuárias

- **Pessoa cliente:** registra e acompanha seus próprios chamados.
- **Pessoa atendente:** consulta, atualiza e encerra chamados.

## Arquitetura

A arquitetura inicial do sistema segue o fluxo:

**Pessoa usuária → Interface Web / Front-end → API → Back-end → Banco de dados**

Como evolução futura, poderá ser adicionado um **Serviço de Notificações**, conforme descrito no diagrama arquitetural.

O diagrama arquitetural completo está disponível em [docs/diagrama-arquitetura.md](docs/diagrama-arquitetura.md).

## Estrutura do projeto

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
