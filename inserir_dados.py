from backend.app.database import engine
from sqlalchemy import text

with engine.connect() as conn:

    # Hospitais
    conn.execute(text("""
        INSERT IGNORE INTO hospitais (nome, provincia, cidade, api_key) VALUES
        ('Hospital Central da Beira', 'Sofala', 'Beira', 'hcb-key-abc123def456'),
        ('Hospital Distrital da Dondo', 'Sofala', 'Dondo', 'hdd-key-xyz789ghi012'),
        ('Clinica Maternidade Esperanca', 'Sofala', 'Beira', 'cme-key-lmn345opq678')
    """))

    # Cidadãos
    conn.execute(text("""
        INSERT IGNORE INTO cidadaos_bi (bi, nome_completo, data_nascimento, sexo, vivo) VALUES
        ('1234567A', 'António Manuel Ferreira', '1985-03-14', 'M', 1),
        ('2345678B', 'Maria Clara dos Santos', '1990-07-22', 'F', 1),
        ('3456789C', 'João Domingos Machava', '1982-11-05', 'M', 1),
        ('4567890D', 'Beatriz Filomena Nhantumbo', '1993-02-18', 'F', 1),
        ('5678901E', 'Carlos Eduardo Muianga', '1978-09-30', 'M', 1),
        ('6789012F', 'Sonia Margarida Cossa', '1988-12-01', 'F', 1),
        ('7890123G', 'Pedro Augusto Zimba', '1975-04-25', 'M', 1),
        ('8901234H', 'Florinda Rosa Bila', '1995-06-10', 'F', 1),
        ('9012345I', 'Helder Francisco Nkomo', '1980-08-17', 'M', 1),
        ('0123456J', 'Graca Ines Tembe', '1987-05-03', 'F', 1),
        ('1111111K', 'Augusto Benedito Cumbe', '1940-01-20', 'M', 0),
        ('2222222L', 'Ermelinda Sofia Chauque', '1955-11-08', 'F', 0),
        ('3333333M', 'Rafael Inocencio Sitoe', '1992-07-14', 'M', 1),
        ('4444444N', 'Lurdes Conceicao Mathe', '1997-03-28', 'F', 1),
        ('5555555O', 'Domingos Feliciano Manjate', '1969-10-11', 'M', 1),
        ('6666666P', 'Anabela Judite Mondlane', '2001-09-05', 'F', 1)
    """))

    conn.commit()
    print("✅ Dados inseridos com sucesso!")
