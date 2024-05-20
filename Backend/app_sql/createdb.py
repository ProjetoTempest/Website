from sqlmodel import create_engine, SQLModel, Session
from schemas import Cargo, IntermediariaUserProducts, Products, ImagesProducts, IntermediariaUserServices, Service, ImagesService, User, Tecnologia, UserTecnologia, RedesSociais, UserRedesSociais

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    session = Session(engine)

    adm = Cargo(name="Administrador", description="Profissional responsável por gerenciar e administrar um sistema, garantindo que ele funcione corretamente e que as informações estejam seguras.")
    session.add(adm)
    session.commit()

    frontend = Cargo(name="Desenvolvedor Frontend", description="Profissional responsável por criar e implementar a interface de usuário de sites e aplicativos web, garantindo uma experiência visual e funcional intuitiva.")
    session.add(frontend)
    session.commit()

    backend = Cargo(name="Desenvolvedor Backend", description="Profissional responsável por criar e implementar a lógica de um sistema, garantindo que ele funcione corretamente e que as informações estejam seguras.")
    session.add(backend)
    session.commit()

    fullstack = Cargo(name="Desenvolvedor Fullstack", description="Profissional responsável por criar e implementar a interface de usuário e a lógica de um sistema, garantindo que ele funcione corretamente e que as informações estejam seguras.")
    session.add(fullstack)
    session.commit()