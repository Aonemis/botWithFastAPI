from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str]
    artikul: Mapped[int] = mapped_column(Integer, unique=True)
    price: Mapped[float]
    rating: Mapped[float]
    all_prod: Mapped[int]

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)