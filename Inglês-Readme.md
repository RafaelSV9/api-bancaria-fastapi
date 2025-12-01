📘 Asynchronous Banking API with FastAPI

An asynchronous RESTful API built with FastAPI, featuring JWT authentication, bank accounts, deposits, withdrawals, and paginated statements.
This project is ideal for learning backend development, demonstrating portfolio skills, and practicing modern API design.

🚀 Features

The API includes:

👤 User registration

🔐 JWT authentication (/auth/login)

🏦 Bank account creation

➕ Deposits

➖ Withdrawals with balance validation

📄 Bank statement with balance summary

📑 Paginated transaction history

🛠️ Technologies Used

Python 3.11+

FastAPI

Uvicorn

SQLAlchemy Async

SQLite with aiosqlite

JWT (python-jose)

fastapi-pagination

📦 How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/your-username/api-bancaria-fastapi.git
cd api-bancaria-fastapi

2️⃣ Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start the server
uvicorn app.main:app --reload


API URL:

Base URL: http://127.0.0.1:8000

Swagger Docs: http://127.0.0.1:8000/docs

🔑 Main Endpoints
Authentication
Method	Route	Description
POST	/auth/signup	Create a new user
POST	/auth/login	Returns a JWT access token
Accounts
Method	Route	Description
POST	/accounts	Creates a bank account for the authenticated user
Transactions
Method	Route	Description
POST	/accounts/{id}/deposit	Make a deposit
POST	/accounts/{id}/withdraw	Withdraw funds (validates available balance)
Statements
Method	Route	Description
GET	/accounts/{id}/transactions	Paginated list of account transactions
GET	/accounts/{id}/statement	Returns current balance + transactions
📏 Business Rules

❌ Transactions cannot have negative or zero amounts

💰 Withdrawals only occur if the account has sufficient balance

🔐 Users can only operate their own accounts

🗂️ Every transaction is linked to a valid account

📄 Pagination implemented using limit and offset

🧪 Possible Future Improvements

Add unit tests with Pytest

Add Docker support (Dockerfile + docker-compose)

Migrate to PostgreSQL for production use

Include PIX / WIRE / TRANSFER modules

Create an admin dashboard

📝 License

This project was created for study purposes and can be freely used, modified, or included in your portfolio.
