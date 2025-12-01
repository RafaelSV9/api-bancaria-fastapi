# API Bancária Assíncrona com FastAPI

Projeto de uma **API REST bancária assíncrona** construída com FastAPI, utilizando autenticação JWT, modelagem de contas e transações e paginação de resultados.

A API permite:

- Cadastro de usuários
- Autenticação via JWT (`/auth/login`)
- Cadastro de contas correntes
- Registro de depósitos e saques
- Exibição de extrato com saldo e lista de transações (com paginação)

---

## Tecnologias utilizadas

- **Python 3.11+**
- **FastAPI**
- **Uvicorn**
- **SQLAlchemy assíncrono**
- **SQLite (aiosqlite)**
- **JWT (python-jose)**
- **fastapi-pagination**

---

## Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/api-bancaria-fastapi.git
cd api-bancaria-fastapi
```

> Substitua `seu-usuario` pelo seu usuário do GitHub.

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

- `http://127.0.0.1:8000`
- Documentação automática (OpenAPI/Swagger): `http://127.0.0.1:8000/docs`

---

## Endpoints principais

### Autenticação

- `POST /auth/signup` – Cria um novo usuário.
- `POST /auth/login` – Retorna um `access_token` JWT para autenticação.

### Contas

- `POST /accounts` – Cria uma conta para o usuário autenticado.

### Transações

- `POST /accounts/{account_id}/deposit` – Realiza um depósito.
- `POST /accounts/{account_id}/withdraw` – Realiza um saque (valida saldo).

### Extrato e transações

- `GET /accounts/{account_id}/transactions` – Lista transações da conta (com paginação `limit` e `offset` via fastapi-pagination).
- `GET /accounts/{account_id}/statement` – Retorna saldo atual + lista de transações, com paginação simples via query params (`limit` e `offset`).

---

## Regras de negócio implementadas

- Não é permitido realizar transações com **valor negativo ou zero**.
- Antes de um saque, o sistema verifica se a conta possui **saldo suficiente**.
- As transações são sempre associadas a uma conta corrente específica.
- Apenas o **dono da conta** pode visualizar e operar em suas contas e transações (controle via JWT).

---

## Melhorias futuras (sugestões)

- Adicionar tipos de operação mais detalhados (TED, DOC, PIX, etc.).
- Implementar testes automatizados (Pytest).
- Adicionar suporte a banco de dados relacional em produção (PostgreSQL).
- Criar dockerização do projeto (`Dockerfile` e `docker-compose.yml`).

---

## Licença

Projeto criado para fins de estudo e prática em FastAPI, APIs assíncronas e autenticação JWT.
Sinta-se à vontade para adaptar, melhorar e usar como portfólio.
