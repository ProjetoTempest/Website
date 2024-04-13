from fastapi import Depends, FastAPI

app = FastAPI()

from .routes import routerUser
app.include_router(routerUser)