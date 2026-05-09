from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.modelos import RegistoNascimento, RegistoObito

router = APIRouter()

@router.get("/verificar/{nuic}")
def verificar_nuic(nuic: str, db: Session = Depends(get_db)):

    # Procurar em nascimentos
    nascimento = db.query(RegistoNascimento).filter(
        RegistoNascimento.nuic == nuic
    ).first()

    if nascimento:
        return {
            "encontrado": True,
            "tipo": "nascimento",
            "nuic": nascimento.nuic,
            "nome_completo": f"{nascimento.nome_completo} {nascimento.apelidos}",
            "data_nascimento": nascimento.data_nascimento.strftime("%d/%m/%Y"),
            "local_nascimento": nascimento.local_nascimento,
            "aprovado_em": nascimento.aprovado_em.strftime("%d/%m/%Y") if nascimento.aprovado_em else "N/A"
        }

    # Procurar em óbitos
    obito = db.query(RegistoObito).filter(
        RegistoObito.nuic_obito == nuic
    ).first()

    if obito:
        return {
            "encontrado": True,
            "tipo": "obito",
            "nuic": obito.nuic_obito,
            "nome_completo": obito.nome_falecido,
            "data_obito": obito.data_obito.strftime("%d/%m/%Y"),
            "local_obito": obito.local_obito,
            "aprovado_em": obito.aprovado_em.strftime("%d/%m/%Y") if obito.aprovado_em else "N/A"
        }

    return {"encontrado": False, "mensagem": "Nenhum registo encontrado com este NUIC"} 
