from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base, Session, joinedload
from sqlalchemy import create_engine, select
from typing import List, Optional

Base = declarative_base()

class Cargo(Base):
    __tablename__ = 'cargo'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

class IntermediariaUserProducts(Base):
    __tablename__ = 'intermediaria_user_products'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    products_id = Column(Integer, ForeignKey('products.id'))

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    value = Column(Float)
    images = relationship("ImagesProducts", back_populates="products")

class ImagesProducts(Base):
    __tablename__ = 'images_products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    path = Column(String, index=True)
    products_id = Column(Integer, ForeignKey('products.id'))
    products = relationship("Products", back_populates="images")

class IntermediariaUserServices(Base):
    __tablename__ = 'intermediaria_user_services'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    service_id = Column(Integer, ForeignKey('service.id'))

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    value = Column(Float)
    # images = relationship("ImagesService", back_populates="service")

class ImagesService(Base):
    __tablename__ = 'images_service'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    path = Column(String, index=True)
    products_id = Column(Integer, ForeignKey('products.id'))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    cargo_id = Column(Integer, ForeignKey('cargo.id'))
    photo = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    password = Column(String)
    cargo = relationship("Cargo")

class Tecnologia(Base):
    __tablename__ = 'tecnologia'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    link = Column(String)
    icon = Column(String)

class UserTecnologia(Base):
    __tablename__ = 'user_tecnologia'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    tecnologia_id = Column(Integer, ForeignKey('tecnologia.id'))

class RedesSociais(Base):
    __tablename__ = 'redes_sociais'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    link = Column(String)
    icon = Column(String)

class UserRedesSociais(Base):    
    __tablename__ = 'user_redes_sociais'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    redes_sociais_id = Column(Integer, ForeignKey('redes_sociais.id'))
