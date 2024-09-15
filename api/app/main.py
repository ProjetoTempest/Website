from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user_routes import router as user_router 
from app.routes.product_route import router as product_router 
from app.routes.service_route import router as service_router
from app.routes.social_route import router as route_Social_Network 
from app.routes.tecnologia_route import router as route_Tecnologia 
from app.routes.user_link_product_route import router as router_user_link_products 
from app.routes.user_link_service_route import router as router_user_link_service 
from app.routes.user_link_tecnologia_route import router as router_user_link_tecnologia 
from app.routes.user_link_social_route import router as router_user_link_social 
from app.routes.login_route import router as route_login
from app.routes.save_image_route import router as routeSaveImg


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  # Adicione o frontend URL se estiver rodando em uma porta diferente
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode especificar domínios específicos em vez de "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(service_router)
app.include_router(route_Social_Network)
app.include_router(route_Tecnologia)
app.include_router(router_user_link_products)
app.include_router(router_user_link_service)
app.include_router(router_user_link_tecnologia)
app.include_router(router_user_link_social)
app.include_router(route_login)
app.include_router(routeSaveImg)
# app.include_router( routeSaveImg)
# app.include_router(routerProduct)
# app.include_router(route_user_link_products)
# app.include_router(routerService)
# app.include_router(route_user_link_services)
# app.include_router(routerSocialNetwork)
# app.include_router(route_user_link_social)
# app.include_router(routerTecnologia)
# app.include_router(route_user_link_tec)
# app.include_router(route_role)
