import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from backend.app.models.modelos import NotificacaoLog
from dotenv import load_dotenv
import os

load_dotenv()

MAILTRAP_HOST = os.getenv("MAILTRAP_HOST")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT"))
MAILTRAP_USER = os.getenv("MAILTRAP_USER")
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS")
MAILTRAP_FROM = os.getenv("MAILTRAP_FROM")

def enviar_email(destinatario: str, assunto: str, mensagem: str):
    try:
        msg = MIMEMultipart()
        msg["From"]    = MAILTRAP_FROM
        msg["To"]      = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(mensagem, "html"))

        with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
            server.starttls()
            server.login(MAILTRAP_USER, MAILTRAP_PASS)
            server.sendmail(MAILTRAP_FROM, destinatario, msg.as_string())

        return {"sucesso": True}

    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

def notificar_pre_registo_criado(db: Session, pre_registo_id: int, tipo: str, contacto: str, email: str, tem_whatsapp: bool):
    if tipo == "nascimento":
        assunto  = "Registo Civil — Pré-registo de Nascimento Criado"
        mensagem = f"""
        <h2>Conservatória do Registo Civil de Beira</h2>
        <p>O pré-registo de nascimento foi criado com sucesso.</p>
        <p><b>Referência:</b> {pre_registo_id}</p>
        <p>Por favor aguarde a aprovação do funcionário do registo civil.</p>
        <p>Em caso de dúvidas, contacte a conservatória.</p>
        """
    else:
        assunto  = "Registo Civil — Pré-registo de Óbito Criado"
        mensagem = f"""
        <h2>Conservatória do Registo Civil de Beira</h2>
        <p>O pré-registo de óbito foi criado com sucesso.</p>
        <p><b>Referência:</b> {pre_registo_id}</p>
        <p>Por favor aguarde a aprovação do funcionário do registo civil.</p>
        <p>Em caso de dúvidas, contacte a conservatória.</p>
        """

    canal        = "pendente"
    estado_envio = "pendente"
    erro         = None

    if email:
        resultado = enviar_email(email, assunto, mensagem)
        canal        = "email"
        estado_envio = "enviado" if resultado["sucesso"] else "falhou"
        erro         = resultado.get("erro")

    log = NotificacaoLog(
        tipo_registo   = tipo,
        pre_registo_id = pre_registo_id,
        canal          = canal,
        destinatario   = email or contacto,
        mensagem       = mensagem,
        com_pdf        = False,
        estado_envio   = estado_envio,
        erro_detalhe   = erro
    )
    db.add(log)
    db.commit()

    return {"canal": canal, "estado": estado_envio}

def notificar_aprovado(db: Session, pre_registo_id: int, tipo: str, email: str, contacto: str, nuic: str):
    assunto  = "Registo Civil — Registo Aprovado!"
    mensagem = f"""
    <h2>Conservatória do Registo Civil de Beira</h2>
    <p>O seu registo foi <b>aprovado</b> com sucesso.</p>
    <p><b>NUIC:</b> {nuic}</p>
    <p>Pode levantar a certidão na conservatória ou aguardar o envio por email.</p>
    """

    canal        = "pendente"
    estado_envio = "pendente"
    erro         = None

    if email:
        resultado = enviar_email(email, assunto, mensagem)
        canal        = "email"
        estado_envio = "enviado" if resultado["sucesso"] else "falhou"
        erro         = resultado.get("erro")

    log = NotificacaoLog(
        tipo_registo   = tipo,
        pre_registo_id = pre_registo_id,
        canal          = canal,
        destinatario   = email or contacto,
        mensagem       = mensagem,
        com_pdf        = False,
        estado_envio   = estado_envio,
        erro_detalhe   = erro
    )
    db.add(log)
    db.commit()

    return {"canal": canal, "estado": estado_envio} 
