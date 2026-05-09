from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base

class Hospital(Base):
    __tablename__ = "hospitais"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String(200), nullable=False)
    provincia = Column(String(100), nullable=False)
    cidade    = Column(String(100), nullable=False)
    api_key   = Column(String(64), unique=True, nullable=False)
    activo    = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

class CidadaoBI(Base):
    __tablename__ = "cidadaos_bi"

    id              = Column(Integer, primary_key=True, index=True)
    bi              = Column(String(20), unique=True, nullable=False)
    nome_completo   = Column(String(200), nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    sexo            = Column(Enum("M", "F"), nullable=False)
    vivo            = Column(Boolean, default=True)

class PreRegistoNascimento(Base):
    __tablename__ = "pre_registos_nascimento"

    id                    = Column(Integer, primary_key=True, index=True)
    hospital_id           = Column(Integer, ForeignKey("hospitais.id"), nullable=False)
    referencia_hospital   = Column(String(100), nullable=False)
    sexo_bebe             = Column(Enum("M", "F"), nullable=False)
    data_nascimento       = Column(DateTime, nullable=False)
    local_nascimento      = Column(String(200), nullable=False)
    bi_pai                = Column(String(20), nullable=True)
    nome_pai              = Column(String(200), nullable=True)
    bi_mae                = Column(String(20), nullable=False)
    nome_mae              = Column(String(200), nullable=False)
    nome_completo_crianca = Column(String(200), nullable=True)
    apelidos_crianca      = Column(String(200), nullable=True)
    nome_avo_paterno      = Column(String(200), nullable=True)
    nome_avo_paterna      = Column(String(200), nullable=True)
    nome_avo_materno      = Column(String(200), nullable=True)
    nome_avo_materna      = Column(String(200), nullable=True)
    nome_declarante       = Column(String(200), nullable=True)
    bi_declarante         = Column(String(20), nullable=True)
    contacto_encarregado  = Column(String(20), nullable=False)
    email_encarregado     = Column(String(200), nullable=True)
    tem_whatsapp          = Column(Boolean, default=False)
    estado                = Column(Enum("incompleto", "aguarda_aprovacao", "aprovado", "rejeitado", "bi_invalido"), default="incompleto")
    motivo_rejeicao       = Column(Text, nullable=True)
    criado_em             = Column(DateTime, default=datetime.utcnow)
    actualizado_em        = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hospital = relationship("Hospital")

class RegistoNascimento(Base):
    __tablename__ = "registos_nascimento"

    id               = Column(Integer, primary_key=True, index=True)
    pre_registo_id   = Column(Integer, ForeignKey("pre_registos_nascimento.id"), unique=True)
    nuic             = Column(String(20), unique=True, nullable=False)
    nome_completo    = Column(String(200), nullable=False)
    apelidos         = Column(String(200), nullable=False)
    sexo             = Column(Enum("M", "F"), nullable=False)
    data_nascimento  = Column(DateTime, nullable=False)
    local_nascimento = Column(String(200), nullable=False)
    nome_pai         = Column(String(200), nullable=True)
    nome_mae         = Column(String(200), nullable=False)
    nome_avo_paterno = Column(String(200), nullable=True)
    nome_avo_paterna = Column(String(200), nullable=True)
    nome_avo_materno = Column(String(200), nullable=True)
    nome_avo_materna = Column(String(200), nullable=True)
    funcionario_nome = Column(String(200), nullable=False)
    aprovado_em      = Column(DateTime, default=datetime.utcnow)
    pdf_path         = Column(String(500), nullable=True)
    pdf_enviado      = Column(Boolean, default=False)

    pre_registo = relationship("PreRegistoNascimento") 
