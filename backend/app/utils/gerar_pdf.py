from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

PASTA_PDFS = "backend/pdfs"

def garantir_pasta():
    if not os.path.exists(PASTA_PDFS):
        os.makedirs(PASTA_PDFS)

def gerar_boletim_nascimento(registo):
    garantir_pasta()

    nome_ficheiro = f"{PASTA_PDFS}/nascimento_{registo.nuic}.pdf"
    doc = SimpleDocTemplate(
        nome_ficheiro,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    estilos = getSampleStyleSheet()
    titulo  = ParagraphStyle("titulo", parent=estilos["Title"], alignment=TA_CENTER, fontSize=14, spaceAfter=6)
    subtitulo = ParagraphStyle("subtitulo", parent=estilos["Normal"], alignment=TA_CENTER, fontSize=11, spaceAfter=4)
    normal  = ParagraphStyle("normal", parent=estilos["Normal"], fontSize=10, spaceAfter=4)
    negrito = ParagraphStyle("negrito", parent=estilos["Normal"], fontSize=10, fontName="Helvetica-Bold")

    conteudo = []

    conteudo.append(Paragraph("REPÚBLICA DE MOÇAMBIQUE", titulo))
    conteudo.append(Paragraph("Conservatória do Registo Civil de Beira", subtitulo))
    conteudo.append(Paragraph("BOLETIM DE NASCIMENTO", titulo))
    conteudo.append(Spacer(1, 0.5*cm))

    dados = [
        ["NUIC:", registo.nuic],
        ["Nome completo:", f"{registo.nome_completo} {registo.apelidos}"],
        ["Sexo:", "Masculino" if registo.sexo == "M" else "Feminino"],
        ["Data de nascimento:", registo.data_nascimento.strftime("%d/%m/%Y")],
        ["Local de nascimento:", registo.local_nascimento],
        ["Nome do pai:", registo.nome_pai or "Não declarado"],
        ["Nome da mãe:", registo.nome_mae],
        ["Avô paterno:", registo.nome_avo_paterno or "Não declarado"],
        ["Avó paterna:", registo.nome_avo_paterna or "Não declarado"],
        ["Avô materno:", registo.nome_avo_materno or "Não declarado"],
        ["Avó materna:", registo.nome_avo_materna or "Não declarado"],
        ["Aprovado por:", registo.funcionario_nome],
        ["Data de registo:", registo.aprovado_em.strftime("%d/%m/%Y %H:%M") if registo.aprovado_em else datetime.utcnow().strftime("%d/%m/%Y %H:%M")],
    ]

    tabela = Table(dados, colWidths=[5*cm, 12*cm])
    tabela.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",    (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.whitesmoke, colors.white]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    conteudo.append(tabela)
    conteudo.append(Spacer(1, 1*cm))
    conteudo.append(Paragraph(f"Beira, {datetime.utcnow().strftime('%d/%m/%Y')}", normal))
    conteudo.append(Spacer(1, 1.5*cm))
    conteudo.append(Paragraph("_________________________________", normal))
    conteudo.append(Paragraph("Conservador do Registo Civil", normal))

    doc.build(conteudo)
    return nome_ficheiro

def gerar_assento_obito(registo):
    garantir_pasta()

    nome_ficheiro = f"{PASTA_PDFS}/obito_{registo.nuic_obito}.pdf"
    doc = SimpleDocTemplate(
        nome_ficheiro,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    estilos  = getSampleStyleSheet()
    titulo   = ParagraphStyle("titulo", parent=estilos["Title"], alignment=TA_CENTER, fontSize=14, spaceAfter=6)
    subtitulo = ParagraphStyle("subtitulo", parent=estilos["Normal"], alignment=TA_CENTER, fontSize=11, spaceAfter=4)
    normal   = ParagraphStyle("normal", parent=estilos["Normal"], fontSize=10, spaceAfter=4)

    conteudo = []

    conteudo.append(Paragraph("REPÚBLICA DE MOÇAMBIQUE", titulo))
    conteudo.append(Paragraph("Conservatória do Registo Civil de Beira", subtitulo))
    conteudo.append(Paragraph("ASSENTO DE ÓBITO", titulo))
    conteudo.append(Spacer(1, 0.5*cm))

    dados = [
        ["NUIC Óbito:", registo.nuic_obito],
        ["Nome do falecido:", registo.nome_falecido],
        ["BI do falecido:", registo.bi_falecido],
        ["Data do óbito:", registo.data_obito.strftime("%d/%m/%Y")],
        ["Local do óbito:", registo.local_obito],
        ["Causa do óbito:", registo.causa_obito or "Não declarada"],
        ["Nome do declarante:", registo.nome_declarante],
        ["Aprovado por:", registo.funcionario_nome],
        ["Data de registo:", registo.aprovado_em.strftime("%d/%m/%Y %H:%M")],
    ]

    tabela = Table(dados, colWidths=[5*cm, 12*cm])
    tabela.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",    (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.whitesmoke, colors.white]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    conteudo.append(tabela)
    conteudo.append(Spacer(1, 1*cm))
    conteudo.append(Paragraph(f"Beira, {datetime.utcnow().strftime('%d/%m/%Y')}", normal))
    conteudo.append(Spacer(1, 1.5*cm))
    conteudo.append(Paragraph("_________________________________", normal))
    conteudo.append(Paragraph("Conservador do Registo Civil", normal))

    doc.build(conteudo)
    return nome_ficheiro 
