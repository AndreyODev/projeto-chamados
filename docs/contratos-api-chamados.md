# Contrato inicial - API de Chamados

## 1. Recurso

- **Nome:** `chamados`
- **Finalidade:** registrar e acompanhar solicitações de suporte técnico.

O recurso `chamados` representa uma solicitação de suporte registrada por uma pessoa cliente.

---

## 2. Formato das mensagens

As requisições e respostas que possuem corpo utilizam o formato JSON.

```http
Content-Type: application/json
```

---

## 3. Atributos

O recurso `chamados` possui os seguintes atributos:

| Atributo                          | Tipo                   | Obrigatório na criação | Descrição                                                                                |
| --------------------------------- | ---------------------- | ---------------------: | ---------------------------------------------------------------------------------------- |
| `id`                              | número inteiro         |                    Não | Identificador único gerado pelo sistema.                                                 |
| `titulo`                          | texto                  |                    Sim | Resumo do problema ou solicitação.                                                       |
| `descricao`                       | texto                  |                    Sim | Detalhamento do problema ou solicitação.                                                 |
| `prioridade`                      | texto                  |                    Sim | Classificação informativa do chamado. Valores aceitos: `baixa`, `media`, `alta`.         |
| `status`                          | texto                  |                    Não | Situação atual do chamado. Valores aceitos: `aberto`, `em_andamento`, `encerrado`.       |
| `cliente_id`                      | número inteiro         |                    Sim | Identificador da pessoa cliente que abriu o chamado.                                     |
| `data_abertura`                   | data/hora ISO 8601     |                    Não | Data e hora em que o chamado foi criado. Gerada automaticamente pelo sistema.            |
| `atendente_ultima_atualizacao_id` | número inteiro ou nulo |                    Não | Identificador da pessoa atendente que realizou a última atualização. Inicia como `null`. |

### 3.1 Valores aceitos

#### Prioridade

O atributo `prioridade` aceita os seguintes valores:

- `baixa`
- `media`
- `alta`

A prioridade possui apenas finalidade informativa.

Nesta versão não existem:

- fila automática;
- ordenação automática por prioridade;
- SLA;
- escalonamento automático.

#### Status

O atributo `status` aceita os seguintes valores:

- `aberto`
- `em_andamento`
- `encerrado`

O status inicial de todo chamado é `aberto`.

A sequência normal de atualização é:

```text
aberto → em_andamento → encerrado
```

Não é permitido pular etapas da sequência normal.

---

## 4. Regras do recurso

1. O `id` é gerado automaticamente pelo sistema.
2. O `status` inicia como `aberto`.
3. A pessoa cliente não informa o `status` durante a criação.
4. A `data_abertura` é gerada automaticamente pelo sistema no momento da criação.
5. O `atendente_ultima_atualizacao_id` inicia como `null`.
6. A `prioridade` possui apenas finalidade informativa.
7. O `PATCH` é utilizado exclusivamente para atualizar o `status` e registrar o atendente responsável pela última atualização.
8. O `PATCH` não pode alterar:
   - `id`;
   - `titulo`;
   - `descricao`;
   - `prioridade`;
   - `cliente_id`;
   - `data_abertura`.
9. Para uma atualização de status, o corpo do `PATCH` deve informar:
   - o novo `status`;
   - o `atendente_ultima_atualizacao_id`.
10. As alterações de status devem respeitar a sequência:
    `aberto → em_andamento → encerrado`.
11. O contrato não define autenticação ou autorização nesta etapa.
12. A regra de que uma pessoa cliente deve consultar somente seus próprios chamados depende de uma forma futura de identificação ou autenticação da pessoa usuária.

---

## 5. Endpoints

| Método   | URI              | Finalidade                       | Parâmetros               | Status previstos    |
| -------- | ---------------- | -------------------------------- | ------------------------ | ------------------- |
| `GET`    | `/chamados`      | Lista chamados                   | Query opcional `status`  | `200`               |
| `GET`    | `/chamados/{id}` | Consulta um chamado específico   | `id` na URI              | `200`, `404`        |
| `POST`   | `/chamados`      | Cria um chamado                  | Corpo JSON               | `201`, `400`        |
| `PATCH`  | `/chamados/{id}` | Atualiza parcialmente um chamado | `id` na URI e corpo JSON | `200`, `400`, `404` |
| `DELETE` | `/chamados/{id}` | Remove um chamado                | `id` na URI              | `204`, `404`        |

---

## 6. Detalhamento dos endpoints

### 6.1 GET /chamados

Lista os chamados registrados no sistema.

#### Parâmetro de consulta opcional

| Parâmetro | Tipo  | Obrigatório | Valores aceitos                       |
| --------- | ----- | ----------: | ------------------------------------- |
| `status`  | texto |         Não | `aberto`, `em_andamento`, `encerrado` |

#### Exemplo de requisição

```http
GET /chamados?status=aberto
```

#### Resposta de sucesso

**HTTP 200 OK**

```json
[
  {
    "id": 101,
    "titulo": "Erro ao acessar o sistema",
    "descricao": "Não consigo fazer login na plataforma.",
    "prioridade": "alta",
    "status": "aberto",
    "cliente_id": 12,
    "data_abertura": "2026-08-19T14:32:00Z",
    "atendente_ultima_atualizacao_id": null
  }
]
```

---

### 6.2 GET /chamados/{id}

Consulta um chamado específico pelo identificador.

#### Parâmetro de rota

| Parâmetro | Tipo           | Obrigatório |
| --------- | -------------- | ----------: |
| `id`      | número inteiro |         Sim |

#### Exemplo de requisição

```http
GET /chamados/101
```

#### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "id": 101,
  "titulo": "Erro ao acessar o sistema",
  "descricao": "Não consigo fazer login na plataforma.",
  "prioridade": "alta",
  "status": "aberto",
  "cliente_id": 12,
  "data_abertura": "2026-08-19T14:32:00Z",
  "atendente_ultima_atualizacao_id": null
}
```

#### Recurso inexistente

**HTTP 404 Not Found**

```json
{
  "erro": "Recurso não encontrado",
  "detalhes": [
    {
      "campo": "id",
      "mensagem": "Não existe chamado com o id informado."
    }
  ]
}
```

---

### 6.3 POST /chamados

Cria um novo chamado.

#### Campos obrigatórios

O corpo da requisição deve conter:

- `titulo`;
- `descricao`;
- `prioridade`;
- `cliente_id`.

Os campos abaixo são gerados ou definidos pelo sistema e não devem ser enviados na criação:

- `id`;
- `status`;
- `data_abertura`;
- `atendente_ultima_atualizacao_id`.

#### Exemplo de requisição

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "titulo": "Erro ao acessar o sistema",
  "descricao": "Não consigo fazer login na plataforma desde esta manhã.",
  "prioridade": "alta",
  "cliente_id": 12
}
```

#### Resposta de sucesso

**HTTP 201 Created**

```http
Location: /chamados/101
```

```json
{
  "id": 101,
  "titulo": "Erro ao acessar o sistema",
  "descricao": "Não consigo fazer login na plataforma desde esta manhã.",
  "prioridade": "alta",
  "status": "aberto",
  "cliente_id": 12,
  "data_abertura": "2026-08-19T14:32:00Z",
  "atendente_ultima_atualizacao_id": null
}
```

---

### 6.4 PATCH /chamados/{id}

Atualiza parcialmente um chamado.

Nesta versão do contrato, o `PATCH` possui finalidade específica: atualizar o status e registrar o atendente responsável pela última atualização.

#### Parâmetro de rota

| Parâmetro | Tipo           | Obrigatório |
| --------- | -------------- | ----------: |
| `id`      | número inteiro |         Sim |

#### Campos aceitos no corpo

| Campo                             | Tipo           | Obrigatório | Descrição                                              |
| --------------------------------- | -------------- | ----------: | ------------------------------------------------------ |
| `status`                          | texto          |         Sim | Novo status do chamado.                                |
| `atendente_ultima_atualizacao_id` | número inteiro |         Sim | Identificador do atendente que realizou a atualização. |

Nenhum outro campo deve ser alterado por este endpoint.

#### Exemplo de requisição

```http
PATCH /chamados/101
Content-Type: application/json
```

```json
{
  "status": "em_andamento",
  "atendente_ultima_atualizacao_id": 7
}
```

#### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "id": 101,
  "titulo": "Erro ao acessar o sistema",
  "descricao": "Não consigo fazer login na plataforma desde esta manhã.",
  "prioridade": "alta",
  "status": "em_andamento",
  "cliente_id": 12,
  "data_abertura": "2026-08-19T14:32:00Z",
  "atendente_ultima_atualizacao_id": 7
}
```

#### Status inválido ou transição inválida

**HTTP 400 Bad Request**

Exemplo de tentativa de alterar diretamente de `aberto` para `encerrado`:

```json
{
  "erro": "Dado inválido",
  "detalhes": [
    {
      "campo": "status",
      "mensagem": "A transição de status informada não é permitida."
    }
  ]
}
```

---

### 6.5 DELETE /chamados/{id}

Remove um chamado pelo identificador.

#### Parâmetro de rota

| Parâmetro | Tipo           | Obrigatório |
| --------- | -------------- | ----------: |
| `id`      | número inteiro |         Sim |

#### Exemplo de requisição

```http
DELETE /chamados/101
```

#### Resposta de sucesso

**HTTP 204 No Content**

A resposta não possui corpo.

#### Recurso inexistente

**HTTP 404 Not Found**

```json
{
  "erro": "Recurso não encontrado",
  "detalhes": [
    {
      "campo": "id",
      "mensagem": "Não existe chamado com o id informado."
    }
  ]
}
```

> **Observação:** o endpoint `DELETE` está presente porque a atividade do laboratório exige a operação de remoção. A exclusão de chamados não foi definida como uma das operações de negócio da V1 na atividade anterior e, por isso, sua utilização real permanece como uma decisão pendente.

---

## 7. Exemplos de erros

### 7.1 Erro 400 - dado obrigatório ausente

Exemplo: criação de chamado sem o campo `titulo`.

#### Requisição

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "descricao": "Não consigo acessar o sistema.",
  "prioridade": "media",
  "cliente_id": 12
}
```

#### Resposta

**HTTP 400 Bad Request**

```json
{
  "erro": "Dado inválido",
  "detalhes": [
    {
      "campo": "titulo",
      "mensagem": "O título é obrigatório."
    }
  ]
}
```

---

### 7.2 Erro 404 - recurso inexistente

Exemplo: consulta de um chamado que não existe.

#### Requisição

```http
GET /chamados/9999
```

#### Resposta

**HTTP 404 Not Found**

```json
{
  "erro": "Recurso não encontrado",
  "detalhes": [
    {
      "campo": "id",
      "mensagem": "Não existe chamado com o id informado."
    }
  ]
}
```

---

## 8. Estrutura padrão de erros

Os erros de validação utilizam a seguinte estrutura:

```json
{
  "erro": "Dado inválido",
  "detalhes": [
    {
      "campo": "nome_do_campo",
      "mensagem": "Descrição compreensível do problema."
    }
  ]
}
```

Os erros de recurso inexistente utilizam:

```json
{
  "erro": "Recurso não encontrado",
  "detalhes": [
    {
      "campo": "id",
      "mensagem": "Não existe chamado com o id informado."
    }
  ]
}
```

---

## 9. Resumo dos códigos HTTP

| Código            | Significado                                 | Utilização                                              |
| ----------------- | ------------------------------------------- | ------------------------------------------------------- |
| `200 OK`          | Operação realizada com sucesso              | Consultas e atualização                                 |
| `201 Created`     | Recurso criado com sucesso                  | Criação de chamado                                      |
| `204 No Content`  | Operação realizada sem conteúdo de resposta | Remoção de chamado                                      |
| `400 Bad Request` | Dados enviados são inválidos                | Validação e transição de status inválida                |
| `404 Not Found`   | Recurso não encontrado                      | Consulta, atualização ou remoção de chamado inexistente |

---

## 10. Decisões e dúvidas pendentes

### Decisões

1. O recurso principal da API é `chamados`.
2. As URIs utilizam nomes de recursos no plural:
   - `/chamados`
   - `/chamados/{id}`
3. O formato das mensagens que possuem corpo é JSON.
4. O status inicial de um chamado é `aberto`.
5. A sequência normal de status é:
   `aberto → em_andamento → encerrado`.
6. O campo `prioridade` possui somente finalidade informativa.
7. Não serão implementados nesta versão:
   - fila automática;
   - SLA;
   - escalonamento;
   - ordenação automática por prioridade;
   - autenticação;
   - notificações.
8. O `PATCH` aceita somente `status` e `atendente_ultima_atualizacao_id`.
9. Os demais dados do chamado não podem ser alterados pelo `PATCH`.

### Dúvidas pendentes

1. O `DELETE` foi incluído por exigência, mas sua utilização como operação de negócio precisa ser validada em relação ao objetivo de manter um histórico básico e confiável dos chamados.
2. A regra da atividade anterior determina que a pessoa cliente deve consultar somente seus próprios chamados. A forma de identificar ou autenticar a pessoa cliente ainda não faz parte e deverá ser definida posteriormente.
3. A autenticação e autorização dos perfis de cliente e atendente serão tratadas em uma etapa posterior.
