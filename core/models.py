# sqlAlchemy models
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)

    user_alert = relationship("Alert", back_populates="alert_user")
    user_passwordreset = relationship(
        "Password_Reset", back_populates="passwordreset_user"
    )


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    asin = Column(String, unique=True)
    title = Column(String)
    currency = Column(String)
    current_amount = Column(Float)
    disabled = Column(Boolean, default=False)  # if no current alerts, disable

    item_alert = relationship("Alert", back_populates="alert_item")
    item_ph = relationship("Price_History", back_populates="ph_item")


class Alert(Base):
    __tablename__ = "alert"

    id = Column(Integer, primary_key=True)
    asin = Column(String, ForeignKey("item.asin"))  # foreign key pointing to items
    user_id = Column(Integer, ForeignKey("user.id"))  # foreign key pointing to users
    target_amount = Column(Float)  # data type - check if it should be float

    alert_user = relationship("User", back_populates="user_alert")
    alert_item = relationship("Item", back_populates="item_alert")


class Price_History(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    asin = Column(String, ForeignKey("item.asin"))  # foreign key pointing to items
    date = Column(Date)
    currency = Column(String)
    amount = Column(Float)

    ph_item = relationship("Item", back_populates="item_ph")


class Password_Reset(Base):
    __tablename__ = "password_reset"

    email = Column(String, ForeignKey("user.email"), primary_key=True)
    token_hash = Column(String)
    expiration = Column(DateTime)
    token_used = Column(Boolean, default=False)

    passwordreset_user = relationship("User", back_populates="user_passwordreset")
