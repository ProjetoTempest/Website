from sqlmodel import Field, SQLModel, Relationship, create_engine, Session, select, String
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

class ProductsBase(SQLModel):
    title: str
    description: Optional[str] = None
    value: float

class Products(ProductsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    images: Optional[List["ImagesProducts"]] = Relationship(back_populates="products")

class ImagesProducts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    path: str
    products_id: int = Field(foreign_key="products.id")
    products: Optional[Products] = Relationship(back_populates="images")


class IntermediariaUserServices(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    service_id: int = Field(foreign_key="service.id")


class ServiceBase(SQLModel):
    title: str
    description: Optional[str] = None
    value: float

class Service(ServiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # images: Optional[List["ImagesService"]] = Relationship(back_populates="service")

class ImagesService(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    path: str
    products_id: int = Field(foreign_key="products.id")

class UserBase(SQLModel):
    name: str
    email: str
    cargo_id: int
    photo: Optional[str] = None
    description: Optional[str] = None 

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    cargo_id: int = Field(foreign_key='cargo.id')


class TecnologiaBase(SQLModel):
    title: str
    description: Optional[str] = None
    link: str
    icon: str

class Tecnologia(TecnologiaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserTecnologia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    tecnologia_id: int = Field(foreign_key="tecnologia.id")


class RedesSociaisBase(SQLModel):
    title: str
    description: Optional[str] = None
    link: str
    icon: str

class RedesSociais(RedesSociaisBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserRedesSociais(SQLModel, table=True):    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    redes_sociais_id: int = Field(foreign_key="redessociais.id")


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
