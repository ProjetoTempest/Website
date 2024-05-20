from sqlmodel import create_engine, SQLModel
from schemas import Cargo, IntermediariaUserProducts, Products, ImagesProducts, IntermediariaUserServices, Service, ImagesService, User, Tecnologia, UserTecnologia, RedesSociais, UserRedesSociais

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)