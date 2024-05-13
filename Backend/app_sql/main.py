from fastapi import Depends, FastAPI

app = FastAPI()

from .routes import routerUser, routerProduct, routerService
app.include_router(routerUser)
app.include_router(routerProduct)
app.include_router(routerService)