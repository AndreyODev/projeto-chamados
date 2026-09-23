# Projeto Chamados

Sistema web de gestão de chamados para uma empresa de suporte técnico.

# Equipe

- [@AndreyODev](https://github.com/AndreyODev)
- [@Cristian-Bryan](https://github.com/Cristian-Bryan)
- [@Gabriell-Bravo](https://github.com/Gabriell-Bravo)
- [@Jeanlukas1](https://github.com/Jeanlukas1)
- [@ThiagoRiey](https://github.com/ThiagoRiey)

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

E o planejamento está disponível em [docs/planejamento-semana-1.md](docs/planejamento-semana-1.md).

## Estrutura do projeto

```text
projeto-chamados/
├── README.md
├── docs/
│   ├── planejamento-semana-1.md
│   ├── diagrama-arquitetura.md
│   ├── modelo-persistencia-chamado.md
│   └── evidencia-testes-persistencia.md
├── database/
│   ├── __init__.py
│   └── connection.py
├── migrations/
│   └── 001_criar_tabela_chamados.sql
├── scripts/
│   └── 001_criar_tabela_chamados.sql
├── frontend/
├── backend/
└── prints/
```

O database local utilizado pela aplicação se chama `chamados`. A conexão é
configurada pelo arquivo `.env`, que não deve ser versionado.

- `database/`: conexão e configuração do acesso ao PostgreSQL.
- `migrations/`: estrutura versionada das entidades persistidas.
- `scripts/`: scripts auxiliares para executar migrations.

## Persistência de chamados

### Modelo simplificado

A entidade `Chamado` é persistida na tabela `chamados` com os campos:

| Campo | Regra |
|---|---|
| `id` | Inteiro gerado pelo banco e usado como identificador único. |
| `titulo` | Texto obrigatório, com até 120 caracteres. |
| `descricao` | Texto obrigatório. |
| `prioridade` | `baixa`, `media` ou `alta`. |
| `status` | `aberto`, `em_andamento` ou `fechado`; inicia como `aberto`. |
| `criado_em` | Data e hora preenchida pelo banco. |

### Migration e preparação do banco

A migration versionada está em
[`migrations/001_criar_tabela_chamados.sql`](migrations/001_criar_tabela_chamados.sql).
O arquivo [`scripts/001_criar_tabela_chamados.sql`](scripts/001_criar_tabela_chamados.sql)
é um auxiliar para execução da migration versionada.

Com o PostgreSQL instalado e em execução, crie o banco `chamados` e aplique a
migration:

```powershell
createdb -U postgres chamados
psql -U postgres -d chamados -f migrations/001_criar_tabela_chamados.sql
```

Se o banco já existir, execute somente o segundo comando. Alternativamente,
o script auxiliar pode ser executado a partir do diretório `scripts`:

```powershell
Set-Location scripts
psql -U postgres -d chamados -f 001_criar_tabela_chamados.sql
Set-Location ..
```

### Variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores da instalação local:

```powershell
Copy-Item .env.example .env
```

As variáveis aceitas são:

- `DATABASE_URL` (opcional); ou
- `DB_HOST` (padrão: `localhost`);
- `DB_PORT` (padrão: `5432`);
- `DB_NAME` (padrão: `chamados`);
- `DB_USER` (padrão: `postgres`);
- `DB_PASSWORD`.

O arquivo `.env` é ignorado pelo Git. Não adicione senhas, tokens ou URLs de
conexão com credenciais ao repositório. Para evitar exposição de credenciais,
use o formato das variáveis em `.env.example` e mantenha os valores reais
somente no ambiente local.

### Endpoints implementados

| Método | Endpoint | Resultado |
|---|---|---|
| `POST` | `/chamados` | Cria um chamado e retorna `201 Created`. |
| `GET` | `/chamados` | Lista chamados persistidos e retorna `200 OK`. |
| `GET` | `/chamados/{id}` | Retorna um chamado e `200 OK`, ou `404 Not Found` quando o id não existe. |

O corpo de criação deve conter `titulo`, `descricao` e `prioridade`. O campo
`status` é opcional e inicia como `aberto`.

### Execução da aplicação

Instale as dependências no ambiente virtual e inicie a API a partir da raiz do
projeto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. A documentação interativa
fica em `http://127.0.0.1:8000/docs`.

### Decisões técnicas e validação

O acesso ao banco foi separado em repository, service, controller e route. O
service não mantém uma lista em memória: as consultas de coleção e por id usam
o repository, que lê os dados diretamente do PostgreSQL. As consultas SQL usam
parâmetros separados dos valores, incluindo a consulta por identificador, para
evitar interpolação de entrada do usuário.

Os schemas do FastAPI validam os campos obrigatórios e os valores permitidos.
Por isso, uma criação sem `titulo` retorna `422 Unprocessable Entity`. Quando o
repository não encontra o id solicitado, a rota retorna `404 Not Found`.

Os fluxos de criação, listagem, consulta por id, reinício da aplicação, erro de
validação, id inexistente e consulta direta no PostgreSQL foram validados. Os
resultados estão registrados em
[`docs/evidencia-testes-persistencia.md`](docs/evidencia-testes-persistencia.md).
