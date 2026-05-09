from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.app.database import get_db
from backend.app.models.modelos import Hospital, PreRegistoObito, RegistoObito
from backend.app.services.validacao import validar_bi_falecido, validar_bi
from backend.app.services.notificacoes import notificar_pre_registo_criado, notificar_aprovado

router = APIRouter()

class DadosObito(BaseModel):
    referencia_hospital: str
    bi_falecido:         str
    nome_falecido:       str
    data_obito:          datetime
    local_obito:         str
    causa_obito:         Optional[str] = None
    nome_declarante:     str
    bi_declarante:       str
    contacto_declarante: str
    email_declarante:    Optional[str] = None
    tem_whatsapp:        bool = False

class DadosAprovacaoObito(BaseModel):
    pre_registo_id:   int
    funcionario_nome: str

class DadosRejeicaoObito(BaseModel):
    pre_registo_id:   int
    funcionario_nome: str
    motivo:           str

def autenticar_hospital(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(
        Hospital.api_key == x_api_key,
        Hospital.activo == True
    ).first()
    if not hospital:
        raise HTTPException(status_code=401, detail="API key inválida ou hospital inactivo")
    return hospital

@router.post("/obitos/registar")
def registar_obito(dados: DadosObito, hospital: Hospital = Depends(autenticar_hospital), db: Session = Depends(get_db)):

    resultado = validar_bi_falecido(db, dados.bi_falecido, dados.nome_falecido)
    if not resultado["valido"]:
        return {"sucesso": False, "erro": resultado["erro"]}

    resultado_dec = validar_bi(db, dados.bi_declarante, dados.nome_declarante)
    if not resultado_dec["valido"]:
        return {"sucesso": False, "erro": resultado_dec["erro"]}

    pre_registo = PreRegistoObito(
        hospital_id         = hospital.id,
        referencia_hospital = dados.referencia_hospital,
        bi_falecido         = dados.bi_falecido,
        nome_falecido       = dados.nome_falecido,
        data_obito          = dados.data_obito,
        local_obito         = dados.local_obito,
        causa_obito         = dados.causa_obito,
        nome_declarante     = dados.nome_declarante,
        bi_declarante       = dados.bi_declarante,
        contacto_declarante = dados.contacto_declarante,
        email_declarante    = dados.email_declarante,
        tem_whatsapp        = dados.tem_whatsapp,
        estado              = "aguarda_aprovacao"
    )

    db.add(pre_registo)
    db.commit()
    db.refresh(pre_registo)

    notificar_pre_registo_criado(
        db             = db,
        pre_registo_id = pre_registo.id,
        tipo           = "obito",
        contacto       = dados.contacto_declarante,
        email          = dados.email_declarante,
        tem_whatsapp   = dados.tem_whatsapp
    )

    return {
        "sucesso":        True,
        "pre_registo_id": pre_registo.id,
        "estado":         "aguarda_aprovacao",
        "mensagem":       "Pré-registo de óbito criado com sucesso"
    }

@router.get("/obitos/lista")
def listar_obitos(estado: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PreRegistoObito)
    if estado:
        query = query.filter(PreRegistoObito.estado == estado)
    registos = query.order_by(PreRegistoObito.criado_em.desc()).all()
    return {"total": len(registos), "registos": registos}

@router.get("/obitos/{id}")
def detalhe_obito(id: int, db: Session = Depends(get_db)):
    registo = db.query(PreRegistoObito).filter(PreRegistoObito.id == id).first()
    if not registo:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    return registo

@router.post("/obitos/aprovar")
def aprovar_obito(dados: DadosAprovacaoObito, db: Session = Depends(get_db)):
    pre_registo = db.query(PreRegistoObito).filter(
        PreRegistoObito.id     == dados.pre_registo_id,
        PreRegistoObito.estado == "aguarda_aprovacao"
    ).first()

    if not pre_registo:
        return {"sucesso": False, "erro": "Pré-registo não encontrado ou não está em aguarda_aprovacao"}

    nuic_obito = f"OBIT-{datetime.utcnow().year}-{str(pre_registo.id).zfill(6)}"

    pre_registo.estado = "aprovado"
    db.flush()

    registo = RegistoObito(
        pre_registo_id   = pre_registo.id,
        nuic_obito       = nuic_obito,
        nome_falecido    = pre_registo.nome_falecido,
        bi_falecido      = pre_registo.bi_falecido,
        data_obito       = pre_registo.data_obito,
        local_obito      = pre_registo.local_obito,
        causa_obito      = pre_registo.causa_obito,
        nome_declarante  = pre_registo.nome_declarante,
        funcionario_nome = dados.funcionario_nome,
        aprovado_em      = datetime.utcnow()
    )

    db.add(registo)
    db.commit()
    db.refresh(registo)

    from backend.app.utils.gerar_pdf import gerar_assento_obito
    pdf_path = gerar_assento_obito(registo)

    registo.pdf_path    = pdf_path
    registo.pdf_enviado = True
    db.commit()

    notificar_aprovado(
        db             = db,
        pre_registo_id = pre_registo.id,
        tipo           = "obito",
        email          = pre_registo.email_declarante,
        contacto       = pre_registo.contacto_declarante,
        nuic           = nuic_obito
    )

    return {
        "sucesso":  True,
        "nuic":     nuic_obito,
        "pdf_path": pdf_path,
        "mensagem": "Óbito aprovado, PDF gerado e notificação enviada"
    }

@router.post("/obitos/rejeitar")
def rejeitar_obito(dados: DadosRejeicaoObito, db: Session = Depends(get_db)):
    pre_registo = db.query(PreRegistoObito).filter(
        PreRegistoObito.id     == dados.pre_registo_id,
        PreRegistoObito.estado == "aguarda_aprovacao"
    ).first()

    if not pre_registo:
        return {"sucesso": False, "erro": "Pré-registo não encontrado ou não está em aguarda_aprovacao"}

    pre_registo.estado          = "rejeitado"
    pre_registo.motivo_rejeicao = dados.motivo
    db.commit()

    return {
        "sucesso":  True,
        "mensagem": "Óbito rejeitado com sucesso"
    }
