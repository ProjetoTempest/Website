from fastapi import Depends, FastAPI

app = FastAPI()

from .routes import routerUser, routerProduct
app.include_router(routerUser)
app.include_router(routerProduct)