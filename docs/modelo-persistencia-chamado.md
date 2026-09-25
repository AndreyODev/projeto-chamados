# Modelo de Persistência - Chamado

## Entidade

A entidade `Chamado` representa uma solicitação de suporte registrada pela API e armazenada de forma persistente no banco de dados PostgreSQL.

## Modelo físico

A tabela `chamados` foi criada pela migration em [`migrations/001_criar_tabela_chamados.sql`](../migrations/001_criar_tabela_chamados.sql) e possui a seguinte estrutura:

```sql
CREATE TABLE chamados (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    descricao TEXT NOT NULL,
    prioridade VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'aberto',
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chamados_prioridade_valida
        CHECK (prioridade IN ('baixa', 'media', 'alta')),
    CONSTRAINT chamados_status_valido
        CHECK (status IN ('aberto', 'em_andamento', 'fechado'))
);
```

## Campos

| Campo | Tipo conceitual | Regra |
|---|---|---|
| `id` | inteiro | Identificador único gerado pelo banco |
| `titulo` | texto | Obrigatório; máximo de 120 caracteres |
| `descricao` | texto | Obrigatório |
| `prioridade` | texto | Obrigatório; valores permitidos: `baixa`, `media`, `alta` |
| `status` | texto | Obrigatório; valores permitidos: `aberto`, `em_andamento`, `fechado` |
| `criado_em` | data e hora | Gerado automaticamente no momento da criação |

## Regras de integridade

- `id` deve identificar unicamente cada chamado.
- `titulo` não pode ser nulo.
- `descricao` não pode ser nula.
- `prioridade` não pode ser nula e deve obedecer ao conjunto permitido.
- `status` não pode ser nulo e deve obedecer ao conjunto permitido.
- `criado_em` deve ser preenchido automaticamente.
- A geração do identificador e da data de criação é responsabilidade do banco de dados.

## Correspondência com a API

A API expõe o recurso `Chamado` com os campos `id`, `titulo`, `descricao`, `prioridade`, `status` e `criado_em`.

O desenho atual considera a compatibilidade entre o contrato HTTP e a modelagem do banco, sem remover campos já utilizados pela API, mantendo `prioridade` e `status` validando o conjunto permitido.

## Decisão técnica

A persistência foi implementada diretamente em repository, com consultas SQL parametrizadas e sem uso de lista em memória para leitura. Essa decisão garante que a consulta por coleção e por identificador reflita o estado real do banco e facilita testes de persistência após reinicialização da aplicação.
