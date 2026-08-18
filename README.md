# Projeto Chamados

Sistema web de gestão de chamados para uma empresa de suporte técnico.

## Objetivo

Planejar uma aplicação web capaz de centralizar o registro, acompanhamento, atualização e encerramento de chamados de suporte, substituindo o controle realizado por planilhas e mensagens dispersas.

## Escopo inicial

A primeira versão do sistema será planejada para permitir:

- Registro de chamados por pessoas clientes;
- Consulta dos próprios chamados pela pessoa cliente;
- Consulta dos chamados pela pessoa atendente;
- Atualização do status dos chamados;
- Encerramento dos chamados.

## Pessoas usuárias

- **Pessoa cliente:** registra e acompanha seus próprios chamados.
- **Pessoa atendente:** consulta, atualiza e encerra chamados.

## Arquitetura

A arquitetura inicial está organizada nas seguintes camadas:

```text
Pessoa usuária
      ↓
Interface Web / Front-end
      ↓
API
      ↓
Back-end / Regras de negócio
      ↓
Banco de dados
```
