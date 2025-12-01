from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator

from .models import TransactionType


# --------- Auth ---------
class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --------- Account ---------
class AccountBase(BaseModel):
    number: str


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int

    class Config:
        from_attributes = True


# --------- Transaction ---------
class TransactionBase(BaseModel):
    amount: float

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
        return v


class DepositCreate(TransactionBase):
    pass


class WithdrawCreate(TransactionBase):
    pass


class TransactionRead(BaseModel):
    id: int
    type: TransactionType
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True


class StatementResponse(BaseModel):
    account: AccountRead
    balance: float
    transactions: List[TransactionRead]
