from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import nascimentos, obitos
from backend.app.database import engine
from backend.app.models import modelos

modelos.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Registo Civil",
    description="API para registo de nascimentos e óbitos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nascimentos.router, prefix="/api", tags=["Nascimentos"])
app.include_router(obitos.router, prefix="/api", tags=["Óbitos"])

@app.get("/")
def raiz():
    return {"mensagem": "Sistema de Registo Civil — API online ✅"}

@app.get("/saude")
def saude():
    return {"estado": "ok"}
