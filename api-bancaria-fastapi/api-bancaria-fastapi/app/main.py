from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination import LimitOffsetPage, Params, add_pagination
from fastapi_pagination.ext.async_sqlalchemy import paginate

from .database import engine, Base, get_session
from .models import User, Account, Transaction, TransactionType
from .schemas import (
    UserCreate,
    UserRead,
    Token,
    AccountCreate,
    AccountRead,
    DepositCreate,
    WithdrawCreate,
    TransactionRead,
    StatementResponse,
)
from .auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)

app = FastAPI(
    title="API Bancária Assíncrona",
    description="API REST assíncrona com FastAPI, JWT, contas e transações bancárias.",
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# --------- Auth ---------
@app.post("/auth/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user_in.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    db_user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60),
    )
    return Token(access_token=access_token)


# --------- Contas ---------
@app.post("/accounts", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_in: AccountCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(Account).where(Account.number == account_in.number))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Já existe uma conta com esse número.")

    db_account = Account(
        number=account_in.number,
        owner_id=current_user.id,
    )
    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)
    return db_account


async def _get_account_or_404(
    account_id: int,
    session: AsyncSession,
    current_user: User,
) -> Account:
    result = await session.execute(select(Account).where(Account.id == account_id))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Conta não pertence ao usuário autenticado.")
    return account


# --------- Transações ---------
@app.post(
    "/accounts/{account_id}/deposit",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
)
async def deposit(
    account_id: int,
    deposit_in: DepositCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    account = await _get_account_or_404(account_id, session, current_user)

    db_tx = Transaction(
        account_id=account.id,
        type=TransactionType.DEPOSIT,
        amount=deposit_in.amount,
    )
    session.add(db_tx)
    await session.commit()
    await session.refresh(db_tx)
    return db_tx


@app.post(
    "/accounts/{account_id}/withdraw",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
)
async def withdraw(
    account_id: int,
    withdraw_in: WithdrawCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    account = await _get_account_or_404(account_id, session, current_user)

    result = await session.execute(
        select(
            func.coalesce(
                func.sum(
                    func.case(
                        (
                            (Transaction.type == TransactionType.DEPOSIT, Transaction.amount),
                            (Transaction.type == TransactionType.WITHDRAW, -Transaction.amount),
                        ),
                        else_=0.0,
                    )
                ),
                0.0,
            )
        ).where(Transaction.account_id == account.id)
    )
    current_balance = float(result.scalar_one())

    if withdraw_in.amount > current_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar o saque.",
        )

    db_tx = Transaction(
        account_id=account.id,
        type=TransactionType.WITHDRAW,
        amount=withdraw_in.amount,
    )
    session.add(db_tx)
    await session.commit()
    await session.refresh(db_tx)
    return db_tx


# --------- Extrato + Paginação ---------
@app.get(
    "/accounts/{account_id}/transactions",
    response_model=LimitOffsetPage[TransactionRead],
)
async def list_transactions(
    account_id: int,
    params: Params = Depends(),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await _get_account_or_404(account_id, session, current_user)

    query = (
        select(Transaction)
        .where(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.desc())
    )

    return await paginate(session, query, params)


@app.get("/accounts/{account_id}/statement", response_model=StatementResponse)
async def get_statement(
    account_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    account = await _get_account_or_404(account_id, session, current_user)

    result_balance = await session.execute(
        select(
            func.coalesce(
                func.sum(
                    func.case(
                        (
                            (Transaction.type == TransactionType.DEPOSIT, Transaction.amount),
                            (Transaction.type == TransactionType.WITHDRAW, -Transaction.amount),
                        ),
                        else_=0.0,
                    )
                ),
                0.0,
            )
        ).where(Transaction.account_id == account.id)
    )
    balance = float(result_balance.scalar_one())

    result_tx = await session.execute(
        select(Transaction)
        .where(Transaction.account_id == account.id)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    transactions = result_tx.scalars().all()

    return StatementResponse(
        account=account,
        balance=balance,
        transactions=transactions,
    )


add_pagination(app)
