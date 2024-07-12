from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


# from .routes import routerProduct, routerService
# from routes.user import routerUser
from .routes.router_user import routerUser
from .routes.router_product import routerProduct
from .routes.router_user_link_product import route_user_link_products
from .routes.router_service import routerService
from .routes.route_user_link_services import route_user_link_services
from .routes.route_social_network import routerSocialNetwork
from .routes.route_user_link_social_network import route_user_link_social
from .routes.route_tecnologia import routerTecnologia
from .routes.route_user_link_tecnologia import route_user_link_tec
from .routes.route_role import route_role

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  # Adicione o frontend URL se estiver rodando em uma porta diferente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routerUser)
app.include_router(routerProduct)
app.include_router(route_user_link_products)
app.include_router(routerService)
app.include_router(route_user_link_services)
app.include_router(routerSocialNetwork)
app.include_router(route_user_link_social)
app.include_router(routerTecnologia)
app.include_router(route_user_link_tec)
app.include_router(route_role)
