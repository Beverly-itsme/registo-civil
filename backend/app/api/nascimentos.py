from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.app.database import get_db
from backend.app.models.modelos import Hospital, PreRegistoNascimento, RegistoNascimento
from backend.app.services.validacao import validar_bi

router = APIRouter()

# --- Schemas (estrutura dos dados recebidos) ---

class DadosFase1(BaseModel):
    referencia_hospital:  str
    sexo_bebe:            str
    data_nascimento:      datetime
    local_nascimento:     str
    bi_mae:               str
    nome_mae:             str
    bi_pai:               Optional[str] = None
    nome_pai:             Optional[str] = None
    contacto_encarregado: str
    email_encarregado:    Optional[str] = None
    tem_whatsapp:         bool = False
    nome_completo_crianca: Optional[str] = None
    apelidos_crianca:     Optional[str] = None

class DadosFase2(BaseModel):
    pre_registo_id:       int
    nome_completo_crianca: str
    apelidos_crianca:     str
    nome_avo_paterno:     Optional[str] = None
    nome_avo_paterna:     Optional[str] = None
    nome_avo_materno:     Optional[str] = None
    nome_avo_materna:     Optional[str] = None
    nome_declarante:      Optional[str] = None
    bi_declarante:        Optional[str] = None

class DadosAprovacao(BaseModel):
    pre_registo_id:  int
    funcionario_nome: str

class DadosRejeicao(BaseModel):
    pre_registo_id:   int
    funcionario_nome: str
    motivo:           str

# --- Autenticação do hospital pela API key ---

def autenticar_hospital(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(
        Hospital.api_key == x_api_key,
        Hospital.activo == True
    ).first()
    if not hospital:
        raise HTTPException(status_code=401, detail="API key inválida ou hospital inactivo")
    return hospital

# --- Endpoints ---

@router.post("/nascimentos/fase1")
def receber_fase1(dados: DadosFase1, hospital: Hospital = Depends(autenticar_hospital), db: Session = Depends(get_db)):

    # Validar BI da mãe
    resultado = validar_bi(db, dados.bi_mae, dados.nome_mae)
    if not resultado["valido"]:
        return {"sucesso": False, "erro": resultado["erro"]}

    # Validar BI do pai se fornecido
    if dados.bi_pai and dados.nome_pai:
        resultado_pai = validar_bi(db, dados.bi_pai, dados.nome_pai)
        if not resultado_pai["valido"]:
            return {"sucesso": False, "erro": resultado_pai["erro"]}

    # Determinar estado inicial
    tem_nome = dados.nome_completo_crianca and dados.apelidos_crianca
    estado = "aguarda_aprovacao" if tem_nome else "incompleto"

    # Criar pré-registo
    pre_registo = PreRegistoNascimento(
        hospital_id           = hospital.id,
        referencia_hospital   = dados.referencia_hospital,
        sexo_bebe             = dados.sexo_bebe,
        data_nascimento       = dados.data_nascimento,
        local_nascimento      = dados.local_nascimento,
        bi_mae                = dados.bi_mae,
        nome_mae              = dados.nome_mae,
        bi_pai                = dados.bi_pai,
        nome_pai              = dados.nome_pai,
        contacto_encarregado  = dados.contacto_encarregado,
        email_encarregado     = dados.email_encarregado,
        tem_whatsapp          = dados.tem_whatsapp,
        nome_completo_crianca = dados.nome_completo_crianca,
        apelidos_crianca      = dados.apelidos_crianca,
        estado                = estado
    )

    db.add(pre_registo)
    db.commit()
    db.refresh(pre_registo)

    return {
        "sucesso":        True,
        "pre_registo_id": pre_registo.id,
        "estado":         pre_registo.estado,
        "mensagem":       "Pré-registo criado com sucesso"
    }

@router.post("/nascimentos/fase2")
def completar_fase2(dados: DadosFase2, hospital: Hospital = Depends(autenticar_hospital), db: Session = Depends(get_db)):

    pre_registo = db.query(PreRegistoNascimento).filter(
        PreRegistoNascimento.id == dados.pre_registo_id,
        PreRegistoNascimento.hospital_id == hospital.id
    ).first()

    if not pre_registo:
        return {"sucesso": False, "erro": "Pré-registo não encontrado"}

    if pre_registo.estado not in ["incompleto"]:
        return {"sucesso": False, "erro": f"Pré-registo já está no estado '{pre_registo.estado}'"}

    pre_registo.nome_completo_crianca = dados.nome_completo_crianca
    pre_registo.apelidos_crianca      = dados.apelidos_crianca
    pre_registo.nome_avo_paterno      = dados.nome_avo_paterno
    pre_registo.nome_avo_paterna      = dados.nome_avo_paterna
    pre_registo.nome_avo_materno      = dados.nome_avo_materno
    pre_registo.nome_avo_materna      = dados.nome_avo_materna
    pre_registo.nome_declarante       = dados.nome_declarante
    pre_registo.bi_declarante         = dados.bi_declarante
    pre_registo.estado                = "aguarda_aprovacao"

    db.commit()

    return {
        "sucesso":  True,
        "estado":   "aguarda_aprovacao",
        "mensagem": "Dados complementares adicionados com sucesso"
    }

@router.get("/nascimentos/lista")
def listar_nascimentos(estado: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PreRegistoNascimento)
    if estado:
        query = query.filter(PreRegistoNascimento.estado == estado)
    registos = query.order_by(PreRegistoNascimento.criado_em.desc()).all()
    return {"total": len(registos), "registos": registos}

@router.get("/nascimentos/{id}")
def detalhe_nascimento(id: int, db: Session = Depends(get_db)):
    registo = db.query(PreRegistoNascimento).filter(PreRegistoNascimento.id == id).first()
    if not registo:
        raise HTTPException(status_code=404, detail="Registo não encontrado")
    return registo

@router.post("/nascimentos/aprovar")
def aprovar_nascimento(dados: DadosAprovacao, db: Session = Depends(get_db)):
    pre_registo = db.query(PreRegistoNascimento).filter(
        PreRegistoNascimento.id == dados.pre_registo_id,
        PreRegistoNascimento.estado == "aguarda_aprovacao"
    ).first()

    if not pre_registo:
        return {"sucesso": False, "erro": "Pré-registo não encontrado ou não está em aguarda_aprovacao"}

    # Gerar NUIC
    nuic = f"NASC-{datetime.utcnow().year}-{str(pre_registo.id).zfill(6)}"

    registo = RegistoNascimento(
        pre_registo_id   = pre_registo.id,
        nuic             = nuic,
        nome_completo    = pre_registo.nome_completo_crianca,
        apelidos         = pre_registo.apelidos_crianca,
        sexo             = pre_registo.sexo_bebe,
        data_nascimento  = pre_registo.data_nascimento,
        local_nascimento = pre_registo.local_nascimento,
        nome_pai         = pre_registo.nome_pai,
        nome_mae         = pre_registo.nome_mae,
        nome_avo_paterno = pre_registo.nome_avo_paterno,
        nome_avo_paterna = pre_registo.nome_avo_paterna,
        nome_avo_materno = pre_registo.nome_avo_materno,
        nome_avo_materna = pre_registo.nome_avo_materna,
        funcionario_nome = dados.funcionario_nome
    )

    pre_registo.estado = "aprovado"
    db.add(registo)
    db.commit()
    db.refresh(registo)

    return {
        "sucesso":  True,
        "nuic":     nuic,
        "mensagem": "Registo aprovado e NUIC gerado com sucesso"
    }

@router.post("/nascimentos/rejeitar")
def rejeitar_nascimento(dados: DadosRejeicao, db: Session = Depends(get_db)):
    pre_registo = db.query(PreRegistoNascimento).filter(
        PreRegistoNascimento.id == dados.pre_registo_id,
        PreRegistoNascimento.estado == "aguarda_aprovacao"
    ).first()

    if not pre_registo:
        return {"sucesso": False, "erro": "Pré-registo não encontrado ou não está em aguarda_aprovacao"}

    pre_registo.estado          = "rejeitado"
    pre_registo.motivo_rejeicao = dados.motivo
    db.commit()

    return {
        "sucesso":  True,
        "mensagem": "Registo rejeitado com sucesso"
    }
