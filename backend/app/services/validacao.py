from sqlalchemy.orm import Session
from backend.app.models.modelos import CidadaoBI

def validar_bi(db: Session, bi: str, nome: str):
    cidadao = db.query(CidadaoBI).filter(CidadaoBI.bi == bi).first()

    if not cidadao:
        return {"valido": False, "erro": f"BI {bi} não encontrado na base de dados"}

    if cidadao.nome_completo.strip().lower() != nome.strip().lower():
        return {"valido": False, "erro": f"Nome não corresponde ao BI {bi}"}

    if not cidadao.vivo:
        return {"valido": False, "erro": f"A pessoa com BI {bi} consta como falecida"}

    return {"valido": True, "erro": None}

def validar_bi_falecido(db: Session, bi: str, nome: str):
    cidadao = db.query(CidadaoBI).filter(CidadaoBI.bi == bi).first()

    if not cidadao:
        return {"valido": False, "erro": f"BI {bi} não encontrado na base de dados"}

    if cidadao.nome_completo.strip().lower() != nome.strip().lower():
        return {"valido": False, "erro": f"Nome não corresponde ao BI {bi}"}

    return {"valido": True, "erro": None}
