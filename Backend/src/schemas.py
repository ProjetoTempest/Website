from sqlmodel import Field, SQLModel, Relationship, create_engine, Session, select, String
from typing import List, Optional

from pydantic import BaseModel
from typing import List, Optional
# from .database import session

class CargoBase(SQLModel):
    name: str
    description: Optional[str] = None

class Cargo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)

class IntermediariaUserProducts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    products_id: int = Field(foreign_key="products.id")

# class ProductsBase(SQLModel):
#     title: str
#     description: Optional[str] = None
#     value: float


# class ImagesProducts(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     path: str
#     products_id: Optional[int] = Field(default=None, foreign_key="products.id")
#     products: Optional["Products"] = Relationship(back_populates="images")

# class Products(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     description: str
#     value: float
#     images: List[ImagesProducts] = Relationship(back_populates="products")







class ImageBase(BaseModel):
    url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    item_id: int
    


class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    value: float

class ProductCreate(ProductBase):
    images: List[ImageCreate] = []

class Product(ProductBase):
    id: int
    images: List[Image] = []


class ProductUpdate(BaseModel):    
    title: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None










class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    value: float

class ServiceCreate(ServiceBase):
    images: List[ImageCreate] = []

class ServiceResponse(ServiceBase):
    id: int
    images: List[ImageCreate] = []

class Service(ServiceBase):
    id: int
    images: List[Image] = []

    # class Config:
    #     orm_mode = True

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None


















class IntermediariaUserServices(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    service_id: int = Field(foreign_key="service.id")


# class ServiceBase(SQLModel):
#     title: str
#     description: Optional[str] = None
#     value: float

# class Service(ServiceBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     # images: Optional[List["ImagesService"]] = Relationship(back_populates="service")

# class ImagesService(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     path: str
#     products_id: int = Field(foreign_key="products.id")




class UserBase(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    role_id: int
    photo: Optional[str] = None
    description: Optional[str] = None

class UserBasePass(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    role_id: int
    photo: Optional[str] = None
    description: Optional[str] = None
    password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    photo: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None




# class User(UserBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     password: str
#     cargo_id: int = Field(foreign_key='cargo.id')


class TecnologiaBase(BaseModel):
    title: str
    description: Optional[str] = None
    link: str
    icon: str

class TecnologiaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    icon: Optional[str] = None


class UserTecnologiaUpdate(BaseModel):
    user_id: Optional[int] = None
    tecnologia_id: Optional[int] = None


# class Tecnologia(TecnologiaBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)

class UserTecnologia(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    tecnologia_id: int = Field(foreign_key="tecnologia.id")


class SocialNetworkBase(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    link: str
    icon: str

class SocialNetworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    icon: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    photo: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None

class UserSocialNetworkUpdate(BaseModel):    
    user_id: Optional[int] = None
    social_network_id: Optional[int] = None

# class SocialNetwork(SocialNetworkBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)

# class UserRedesSociais(SQLModel, table=True):    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id")
#     redes_sociais_id: int = Field(foreign_key="redessociais.id")







class RoleBase(BaseModel):
    name: str
    description: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class Role(RoleBase):
    id: int






















# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# engine = create_engine(sqlite_url)

# SQLModel.metadata.create_all(engine)

# # session = Session(engine)

# # cargo1 = Cargo(name="Administrador", description="Acesso total ao sistema")
# # user1 = User(name="Administrador", email="email", photo="fto", description='despro', password="123", cargo_id=1)

# # session.add(user1)
# # session.add(cargo1)

# # session.commit()

# # a = UserBase(session.refresh(user1))
# # print(a)

# with Session(engine) as session:
#     statement = select(User).where(User.id == 1)
#     results = session.exec(statement).first()
#     # print(results)

#     user_data = results.__fields__
#     user_data = dict(user_data)
#     user_data.pop('cargo_id')
#     user_data.pop("password")

#     # a = UserBase(**user_data)
#     # print(a)
#     print(user_data)

# if __name__ == "__main__":
#     statement = select(User).where(User.id == 1)
#     results = session.exec(statement).first()
#     # print(results)

#     user_data = results.__fields__
#     user_data = dict(user_data)
#     user_data.pop('cargo_id')
#     user_data.pop("password")

#     # a = UserBase(**user_data)
#     # print(a)
#     print(user_data)
