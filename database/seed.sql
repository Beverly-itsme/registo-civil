 -- ============================================================
--  DADOS DE TESTE — Hospitais e Cidadãos Fictícios
--  Execute DEPOIS do schema.sql
-- ============================================================

USE registo_civil;

-- HOSPITAIS DE TESTE
INSERT INTO hospitais (nome, provincia, cidade, api_key) VALUES
  ('Hospital Central da Beira',     'Sofala', 'Beira',  'hcb-key-abc123def456'),
  ('Hospital Distrital da Dondo',   'Sofala', 'Dondo',  'hdd-key-xyz789ghi012'),
  ('Clínica Maternidade Esperança', 'Sofala', 'Beira',  'cme-key-lmn345opq678');

-- CIDADÃOS FICTÍCIOS (para validação de BI)
INSERT INTO cidadaos_bi (bi, nome_completo, data_nascimento, sexo, vivo) VALUES
  ('1234567A', 'António Manuel Ferreira',    '1985-03-14', 'M', TRUE),
  ('2345678B', 'Maria Clara dos Santos',     '1990-07-22', 'F', TRUE),
  ('3456789C', 'João Domingos Machava',      '1982-11-05', 'M', TRUE),
  ('4567890D', 'Beatriz Filomena Nhantumbo', '1993-02-18', 'F', TRUE),
  ('5678901E', 'Carlos Eduardo Muianga',     '1978-09-30', 'M', TRUE),
  ('6789012F', 'Sónia Margarida Cossa',      '1988-12-01', 'F', TRUE),
  ('7890123G', 'Pedro Augusto Zimba',        '1975-04-25', 'M', TRUE),
  ('8901234H', 'Florinda Rosa Bila',         '1995-06-10', 'F', TRUE),
  ('9012345I', 'Hélder Francisco Nkomo',     '1980-08-17', 'M', TRUE),
  ('0123456J', 'Graça Inês Tembe',           '1987-05-03', 'F', TRUE),
  ('1111111K', 'Augusto Benedito Cumbe',     '1940-01-20', 'M', FALSE),
  ('2222222L', 'Ermelinda Sofia Chaúque',    '1955-11-08', 'F', FALSE),
  ('3333333M', 'Rafael Inocêncio Sitoe',     '1992-07-14', 'M', TRUE),
  ('4444444N', 'Lurdes Conceição Mathe',     '1997-03-28', 'F', TRUE),
  ('5555555O', 'Domingos Feliciano Manjate', '1969-10-11', 'M', TRUE),
  ('6666666P', 'Anabela Judite Mondlane',    '2001-09-05', 'F', TRUE);
