from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Registo Civil",
    description="API para registo de nascimentos e óbitos",
    version="1.0.0"
)

# Permite o frontend React comunicar com o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def raiz():
    return {"mensagem": "Sistema de Registo Civil — API online ✅"}

@app.get("/saude")
def saude():
    return {"estado": "ok"}
