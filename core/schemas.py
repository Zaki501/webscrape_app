# pydantic schemas
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ResetToken(BaseModel):
    email: str
    token: str


############ User


class UserPassword(BaseModel):
    password: str


class UserBase(BaseModel):
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


############ Password Reset
class Password_Reset(BaseModel):
    email: str
    token_hash: str
    expiration: date
    token_used: bool


######## Tables for database


class ItemCreate(BaseModel):
    asin: str
    title: str
    currency: str
    current_amount: Decimal
    disabled: bool


class Item(ItemCreate):
    id: int


class Alert(BaseModel):
    id: int
    asin: str
    id: int
    target_amount: Decimal


class Price_History(BaseModel):
    id: int
    asin: str
    date: date
    currency: str
    amount: Decimal
