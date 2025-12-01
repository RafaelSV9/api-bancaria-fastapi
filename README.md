📘 API Bancária Assíncrona com FastAPI

Projeto de uma API REST bancária assíncrona construída com FastAPI, utilizando autenticação JWT, contas, transações bancárias e paginação de resultados.
Ideal para estudos, portfólio e evolução em desenvolvimento backend moderno.

🚀 Funcionalidades

A API permite:

👤 Cadastro de usuários

🔐 Autenticação via JWT (/auth/login)

🏦 Criação de contas correntes

➕ Depósitos

➖ Saques (com validação de saldo)

📄 Extrato bancário completo

📑 Lista paginada de transações

🛠️ Tecnologias utilizadas

Python 3.11+

FastAPI

Uvicorn

SQLAlchemy (assíncrono)

SQLite com aiosqlite

JWT (python-jose)

fastapi-pagination

📦 Como rodar o projeto
1️⃣ Clonar Repositório
git clone https://github.com/seu-usuario/api-bancaria-fastapi.git
cd api-bancaria-fastapi

2️⃣ Criar ambiente virtual (recomendado)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Rodar o servidor
uvicorn app.main:app --reload


A API ficará disponível em:

👉 http://127.0.0.1:8000

👉 Documentação Swagger: http://127.0.0.1:8000/docs

🔑 Endpoints principais
Autenticação
Método	Rota	Descrição
POST	/auth/signup	Cria um novo usuário
POST	/auth/login	Retorna JWT para autenticação
Contas
Método	Rota	Descrição
POST	/accounts	Cria uma conta para o usuário autenticado
Transações
Método	Rota	Descrição
POST	/accounts/{id}/deposit	Realiza um depósito
POST	/accounts/{id}/withdraw	Realiza um saque (valida saldo)
Extrato e histórico
Método	Rota	Descrição
GET	/accounts/{id}/transactions	Lista transações com paginação
GET	/accounts/{id}/statement	Saldo atual + lista de transações
📏 Regras de Negócio Implementadas

❌ Não permite transações com valor negativo ou zero

💰 Saque só ocorre se houver saldo suficiente

🔐 Apenas o dono da conta pode acessar ou operar nela

🗂️ Transações são sempre vinculadas a uma conta existente

📑 Paginação com limit e offset via fastapi-pagination

🧪 Melhorias Futuras (opcional)

Testes automatizados com Pytest

Dockerfile + docker-compose

Suporte para PostgreSQL

Módulos de PIX / DOC / TED

Painel administrativo

📄 Licença

Projeto criado para fins de estudo — sinta-se livre para usar, modificar e adicionar ao portfólio.
