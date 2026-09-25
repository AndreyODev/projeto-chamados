# Evidencia de testes de persistencia

Data da execucao: 2026-09-23
Branch: `test/19-validacao-persistencia`
API: `http://127.0.0.1:8000`
Banco: PostgreSQL, database `chamados`

## Cenario de sucesso

### Criacao de chamado

Requisicao: `POST /chamados`

Resultado: `201 Created`

Identificador retornado: `3`

```json
{
  "id": 3,
  "titulo": "Teste validacao persistencia",
  "descricao": "Chamado criado para validar os fluxos do cartao 19",
  "prioridade": "alta",
  "status": "aberto",
  "criado_em": "2026-09-23T09:47:50.542879"
}
```

### Listagem

Requisicao: `GET /chamados`

Resultado: `200 OK`, com o chamado de id `3` presente na colecao.

### Consulta por identificador

Requisicao: `GET /chamados/3`

Resultado: `200 OK`, retornando o chamado correspondente ao id solicitado.

### Persistencia apos reinicio

A aplicacao foi reiniciada e a requisicao `GET /chamados` foi executada novamente.

Resultado: `200 OK`, com o chamado de id `3` ainda presente na colecao.

## Cenarios de erro

### Campo obrigatorio ausente

Requisicao: `POST /chamados`, sem o campo `titulo`.

Resultado: `400 Bad Request`, com detalhe padronizado de campo obrigatorio ausente.

### Identificador inexistente

Requisicao: `GET /chamados/999999999`

Resultado: `404 Not Found`, com a mensagem `Chamado não encontrado`.

## Consulta direta no banco

Consulta executada:

```sql
SELECT id, titulo, descricao, prioridade, status
FROM chamados
WHERE id = 3;
```

Resultado encontrado:

```text
id=3
titulo=Teste validacao persistencia
descricao=Chamado criado para validar os fluxos do cartao 19
prioridade=alta
status=aberto
```

Conclusao: o registro criado pela API foi gravado no PostgreSQL e permaneceu disponivel depois do reinicio da aplicacao.