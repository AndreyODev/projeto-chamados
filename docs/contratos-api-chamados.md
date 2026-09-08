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

| Atributo                          | Tipo                   | Obrigatório na criação | Descrição                                                                                                                |
| --------------------------------- | ---------------------- | ---------------------: | ------------------------------------------------------------------------------------------------------------------------ |
| `id`                              | número inteiro         |                    Não | Identificador único gerado pelo sistema.                                                                                 |
| `titulo`                          | texto                  |                    Sim | Resumo do problema ou solicitação.                                                                                       |
| `descricao`                       | texto                  |                    Sim | Detalhamento do problema ou solicitação.                                                                                 |
| `prioridade`                      | texto                  |                    Sim | Classificação informativa do chamado. Valores aceitos: `baixa`, `media`, `alta`.                                         |
| `status`                          | texto                  |                    Não | Situação atual do chamado. Valores aceitos: `aberto`, `em_andamento`, `encerrado`.                                       |
| `cliente_id`                      | número inteiro         |        Não nesta etapa | Identificador da pessoa cliente que abriu o chamado. A identificação da pessoa cliente será definida em etapa posterior. |
| `data_abertura`                   | data/hora ISO 8601     |                    Não | Data e hora em que o chamado foi criado. Gerada automaticamente pelo sistema.                                            |
| `atendente_ultima_atualizacao_id` | número inteiro ou nulo |                    Não | Identificador da pessoa atendente que realizou a última atualização. Inicia como `null`.                                 |

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

## 5. Escopo da implementação da Etapa 3

A Etapa 3 possui como objetivo implementar uma versão inicial da API antes da utilização de banco de dados.

Nesta etapa serão implementados somente:

- `GET /chamados`
- `POST /chamados`

Os dados serão mantidos temporariamente em memória, utilizando uma coleção da própria aplicação.

### 5.1 Dados utilizados na criação na Etapa 3

O `POST /chamados` da Etapa 3 receberá somente:

- `titulo`;
- `descricao`;
- `prioridade`.

O campo `cliente_id` permanece no modelo geral do recurso, porém **não será obrigatório nem utilizado no cadastro da Etapa 3**.

Essa decisão foi tomada porque o laboratório da Etapa 3 não inclui autenticação ou identificação da pessoa cliente e apresenta o corpo do cadastro somente com `titulo`, `descricao` e `prioridade`.

### 5.2 Identificador temporário

Durante a Etapa 3, o identificador do chamado será gerado de forma simples pela aplicação.

O identificador é temporário e poderá ser substituído posteriormente por uma estratégia adequada de persistência quando o banco de dados for implementado.

### 5.3 Dados fora da implementação da Etapa 3

Os seguintes campos continuam fazendo parte do modelo geral do recurso, mas não serão implementados nesta etapa:

- `status`;
- `cliente_id`;
- `data_abertura`;
- `atendente_ultima_atualizacao_id`.

A implementação desses campos será definida nas etapas posteriores do projeto.

### 5.4 Validações da Etapa 3

O back-end deverá validar:

- presença de `titulo`;
- presença de `descricao`;
- presença de `prioridade`;
- validade do valor informado em `prioridade`.

As prioridades permitidas são:

- `baixa`;
- `media`;
- `alta`.

Dados inválidos deverão resultar em:

**HTTP 400 Bad Request**

com resposta no formato padronizado de erro definido neste contrato.

---

## 6. Endpoints

| Método   | URI              | Finalidade                       | Parâmetros               | Status previstos    |
| -------- | ---------------- | -------------------------------- | ------------------------ | ------------------- |
| `GET`    | `/chamados`      | Lista chamados                   | Query opcional `status`  | `200`               |
| `GET`    | `/chamados/{id}` | Consulta um chamado específico   | `id` na URI              | `200`, `404`        |
| `POST`   | `/chamados`      | Cria um chamado                  | Corpo JSON               | `201`, `400`        |
| `PATCH`  | `/chamados/{id}` | Atualiza parcialmente um chamado | `id` na URI e corpo JSON | `200`, `400`, `404` |
| `DELETE` | `/chamados/{id}` | Remove um chamado                | `id` na URI              | `204`, `404`        |

### 6.1 Endpoints implementados na Etapa 3

Nesta etapa, somente os seguintes endpoints serão implementados:

```text
GET /chamados
POST /chamados
```

Os demais endpoints permanecem definidos no contrato geral para orientar a evolução futura da API.

---

## 7. Detalhamento dos endpoints

### 7.1 GET /chamados

Lista os chamados registrados no sistema.

Na Etapa 3, a consulta retorna todos os chamados armazenados na coleção em memória.

#### Parâmetro de consulta opcional

| Parâmetro | Tipo  | Obrigatório | Valores aceitos                       |
| --------- | ----- | ----------: | ------------------------------------- |
| `status`  | texto |         Não | `aberto`, `em_andamento`, `encerrado` |

> **Observação:** o filtro por `status` permanece previsto no contrato geral, mas não é obrigatório para a implementação mínima da Etapa 3.

#### Exemplo de requisição

```http
GET /chamados
```

#### Resposta de sucesso

**HTTP 200 OK**

A resposta deve ser sempre uma lista JSON, inclusive quando não houver chamados cadastrados.

Exemplo com chamados:

```json
[
  {
    "id": "1",
    "titulo": "Não consigo acessar o sistema",
    "descricao": "A tela de autenticação informa que minhas credenciais são inválidas.",
    "prioridade": "alta"
  }
]
```

Exemplo sem chamados:

```json
[]
```

---

### 7.2 GET /chamados/{id}

Consulta um chamado específico pelo identificador.

#### Parâmetro de rota

| Parâmetro | Tipo                             | Obrigatório |
| --------- | -------------------------------- | ----------: |
| `id`      | número inteiro ou texto numérico |         Sim |

#### Exemplo de requisição

```http
GET /chamados/1
```

#### Resposta de sucesso

**HTTP 200 OK**

```json
{
  "id": 1,
  "titulo": "Erro ao acessar o sistema",
  "descricao": "Não consigo fazer login na plataforma.",
  "prioridade": "alta"
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

> **Observação:** o endpoint `GET /chamados/{id}` faz parte do contrato geral, mas não está entre os endpoints obrigatórios de implementação da Etapa 3.

---

### 7.3 POST /chamados

Cria um novo chamado.

Na Etapa 3, o cadastro recebe somente os campos necessários para a criação inicial do chamado.

#### Campos obrigatórios na Etapa 3

O corpo da requisição deve conter:

- `titulo`;
- `descricao`;
- `prioridade`.

Os seguintes campos não devem ser enviados na criação da Etapa 3:

- `id`;
- `status`;
- `cliente_id`;
- `data_abertura`;
- `atendente_ultima_atualizacao_id`.

#### Exemplo de requisição válida

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "titulo": "Não consigo acessar o sistema",
  "descricao": "A tela de autenticação informa que minhas credenciais são inválidas.",
  "prioridade": "alta"
}
```

#### Resposta de sucesso

**HTTP 201 Created**

```json
{
  "id": "1",
  "titulo": "Não consigo acessar o sistema",
  "descricao": "A tela de autenticação informa que minhas credenciais são inválidas.",
  "prioridade": "alta"
}
```

O identificador retornado é temporário e gerado pela aplicação durante a utilização da coleção em memória.

---

### 7.4 PATCH /chamados/{id}

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

> **Observação:** o endpoint `PATCH /chamados/{id}` não será implementado na Etapa 3.

---

### 7.5 DELETE /chamados/{id}

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

> **Observação:** o endpoint `DELETE` está presente porque a atividade da Etapa 2 exige a operação de remoção. A exclusão de chamados não foi definida como uma das operações de negócio da V1 na atividade anterior e não será implementada na Etapa 3.

---

## 8. Exemplos de erros

### 8.1 Erro 400 - título ausente

Exemplo: criação de chamado sem o campo `titulo`.

#### Requisição

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "descricao": "Não consigo acessar o sistema.",
  "prioridade": "media"
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

### 8.2 Erro 400 - descrição ausente

#### Requisição

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "titulo": "Erro ao acessar o sistema",
  "prioridade": "alta"
}
```

#### Resposta

**HTTP 400 Bad Request**

```json
{
  "erro": "Dado inválido",
  "detalhes": [
    {
      "campo": "descricao",
      "mensagem": "A descrição é obrigatória."
    }
  ]
}
```

---

### 8.3 Erro 400 - prioridade inválida

#### Requisição

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "titulo": "Erro ao acessar o sistema",
  "descricao": "Não consigo fazer login na plataforma.",
  "prioridade": "urgente"
}
```

#### Resposta

**HTTP 400 Bad Request**

```json
{
  "erro": "Dado inválido",
  "detalhes": [
    {
      "campo": "prioridade",
      "mensagem": "Use baixa, media ou alta."
    }
  ]
}
```

---

### 8.4 Erro 404 - recurso inexistente

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

## 9. Estrutura padrão de erros

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

Na Etapa 3, todos os erros de validação do `POST /chamados` devem utilizar o mesmo formato.

---

## 10. Resumo dos códigos HTTP

| Código            | Significado                                 | Utilização                                              |
| ----------------- | ------------------------------------------- | ------------------------------------------------------- |
| `200 OK`          | Operação realizada com sucesso              | Consultas e atualização                                 |
| `201 Created`     | Recurso criado com sucesso                  | Criação de chamado                                      |
| `204 No Content`  | Operação realizada sem conteúdo de resposta | Remoção de chamado                                      |
| `400 Bad Request` | Dados enviados são inválidos                | Validação e transição de status inválida                |
| `404 Not Found`   | Recurso não encontrado                      | Consulta, atualização ou remoção de chamado inexistente |

---

## 11. Decisões e dúvidas pendentes

### 11.1 Decisões

1. O recurso principal da API é `chamados`.

2. As URIs utilizam nomes de recursos no plural:
   - `/chamados`
   - `/chamados/{id}`

3. O formato das mensagens que possuem corpo é JSON.

4. O status inicial de um chamado é `aberto`.

5. A sequência normal de status é:

   `aberto → em_andamento → encerrado`

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

10. Na Etapa 3, os dados serão mantidos em memória.

11. Na Etapa 3, serão implementados somente:
    - `GET /chamados`;
    - `POST /chamados`.

12. Na Etapa 3, o `POST /chamados` recebe somente:
    - `titulo`;
    - `descricao`;
    - `prioridade`.

13. O `cliente_id` permanece no modelo geral do recurso, mas não será obrigatório nem utilizado no cadastro da Etapa 3.

14. O identificador utilizado na Etapa 3 será temporário e gerado pela própria aplicação.

15. A regra de prioridade será validada no back-end e aceitará somente:
    - `baixa`;
    - `media`;
    - `alta`.

16. Os erros de validação da Etapa 3 utilizarão uma estrutura padronizada.

### 11.2 Dúvidas pendentes

1. O `DELETE` foi incluído no contrato por exigência da atividade anterior, mas sua utilização como operação de negócio precisa ser validada em relação ao objetivo de manter um histórico básico e confiável dos chamados.

2. A regra da atividade anterior determina que a pessoa cliente deve consultar somente seus próprios chamados. A forma de identificar ou autenticar a pessoa cliente ainda não faz parte desta etapa e deverá ser definida posteriormente.

3. A autenticação e autorização dos perfis de cliente e atendente serão tratadas em uma etapa posterior.

4. A estratégia definitiva de geração de identificadores e persistência dos chamados será definida quando o banco de dados for introduzido no projeto.

---

## 12. Escopo futuro

Este contrato representa a evolução inicial da API de Chamados.

As próximas etapas poderão implementar:

- persistência em banco de dados;
- autenticação;
- autorização por perfil;
- identificação da pessoa cliente;
- consulta dos chamados associados à pessoa cliente;
- atualização de status;
- identificação do atendente responsável;
- histórico das alterações;
- demais endpoints previstos neste contrato.

As funcionalidades futuras não devem ser implementadas antecipadamente sem que sejam definidas em uma etapa correspondente do projeto.
