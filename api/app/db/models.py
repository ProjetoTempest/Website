from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from db.base import Base

class Role(Base):
    __tablename__ = 'role'
    id:Mapped[str] = mapped_column(String, primary_key=True)
    name:Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description:Mapped[str] = mapped_column(String, nullable=True)

class IntermediariaUserProducts(Base):
    __tablename__ = 'intermediaria_user_products'
    id:Mapped[str] = mapped_column(Integer, primary_key=True, index=True)
    user_id:Mapped[str] = mapped_column(Integer, ForeignKey('user.id'))
    products_id = mapped_column(Integer, ForeignKey('products.id'))

class Products(Base):
    __tablename__ = 'products'
    id:Mapped[str] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String, index=True)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    value:Mapped[str] = mapped_column(Float, nullable=False)
    images = relationship("ImagesProducts", back_populates="products")

class Products(Base):
    __tablename__ = 'products'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    images = relationship("ImagesProducts", back_populates="products")

class ImagesProducts(Base):
    __tablename__ = 'images_products'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, index=True)
    item_id: Mapped[str] = mapped_column(String, ForeignKey('products.id'))
    products = relationship("Products", back_populates="images")

class IntermediariaUserServices(Base):
    __tablename__ = 'intermediaria_user_services'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('user.id'))
    service_id: Mapped[str] = mapped_column(String, ForeignKey('service.id'))

class Service(Base):
    __tablename__ = 'service'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    value: Mapped[float] = mapped_column(Float)
    images = relationship("ImagesService", back_populates="service")

class ImagesService(Base):
    __tablename__ = 'images_service'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, index=True)
    item_id: Mapped[str] = mapped_column(String, ForeignKey('service.id'))
    service = relationship("Service", back_populates="images")

class User(Base):
    __tablename__ = 'user'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True)
    role_id: Mapped[str] = mapped_column(String, ForeignKey('role.id'))
    photo: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String)
    role = relationship("Role", back_populates="users")

class Role(Base):
    __tablename__ = 'role'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    users = relationship("User", back_populates="role")

class Tecnologia(Base):
    __tablename__ = 'tecnologia'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    link: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String)

class UserTecnologia(Base):
    __tablename__ = 'user_tecnologia'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('user.id'))
    tecnologia_id: Mapped[str] = mapped_column(String, ForeignKey('tecnologia.id'))

class SocialNetwork(Base):
    __tablename__ = 'social_network'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    link: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String)

class UserSocialNetwork(Base):
    __tablename__ = 'user_social_network'
    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('user.id'))
    social_network_id: Mapped[str] = mapped_column(String, ForeignKey('social_network.id'))