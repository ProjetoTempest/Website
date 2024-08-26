from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
# from src.database import Base

class Role(Base):
    __tablename__ = 'role'
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
    url = Column(String, index=True)
    item_id = Column(Integer, ForeignKey('products.id'))
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
    images = relationship("ImagesService", back_populates="service")

class ImagesService(Base):
    __tablename__ = 'images_service'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    item_id = Column(Integer, ForeignKey('service.id'))
    service = relationship("Service", back_populates="images")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    photo = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    password = Column(String)
    role = relationship("Role")

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

class SocialNetwork(Base):
    __tablename__ = 'social_network'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    link = Column(String)
    icon = Column(String)

class UserSocialNetwork(Base):    
    __tablename__ = 'user_social_network'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    social_network_id = Column(Integer, ForeignKey('social_network.id'))
