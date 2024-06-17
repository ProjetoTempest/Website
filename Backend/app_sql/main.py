from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import routerUser, routerProduct, routerService


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )

# @app.get("/cadastro.html")
# async def get_cadastro(request: Request):
#     return Jinja2Templates.TemplateResponse("cadastro.html", {"request": request})


templates = Jinja2Templates(directory="/home/will/Documentos/project_tempest/Website/Backend/app_sql/templates")

@app.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})




from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(routerService)