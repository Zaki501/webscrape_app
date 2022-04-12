# pydantic schemas
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


############ User


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


######## Tables for database


class Item(BaseModel):
    asin: str
    title: str
    currency: str
    current_amount: Decimal
    disabled: bool


class Alert(BaseModel):
    asin: str
    id: int
    target_amount: Decimal


class Price_History(BaseModel):
    asin: str
    date: date
    currency: str
    amount: Decimal
