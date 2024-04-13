from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(11), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    cargo = Column(String)
    photo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    # products = relationship("Products", back_populates="owner")


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    value = Column(Float)
    images = Column(String, nullable=True)
    # owner = relationship("User", back_populates="items")
    # disponivel = Column(Boolean, default=True)