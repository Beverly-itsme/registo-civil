-- ============================================================
--  SISTEMA DE REGISTO CIVIL — Base de Dados MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS registo_civil
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE registo_civil;

-- TABELA 1 — HOSPITAIS
CREATE TABLE IF NOT EXISTS hospitais (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nome          VARCHAR(200)  NOT NULL,
  provincia     VARCHAR(100)  NOT NULL,
  cidade        VARCHAR(100)  NOT NULL,
  api_key       VARCHAR(64)   NOT NULL UNIQUE,
  activo        BOOLEAN       NOT NULL DEFAULT TRUE,
  criado_em     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- TABELA 2 — CIDADÃOS (validação de BI)
CREATE TABLE IF NOT EXISTS cidadaos_bi (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  bi              VARCHAR(20)   NOT NULL UNIQUE,
  nome_completo   VARCHAR(200)  NOT NULL,
  data_nascimento DATE          NOT NULL,
  sexo            ENUM('M','F') NOT NULL,
  vivo            BOOLEAN       NOT NULL DEFAULT TRUE,
  criado_em       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- TABELA 3 — PRÉ-REGISTOS DE NASCIMENTO
CREATE TABLE IF NOT EXISTS pre_registos_nascimento (
  id                    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  hospital_id           INT UNSIGNED  NOT NULL,
  referencia_hospital   VARCHAR(100)  NOT NULL,
  sexo_bebe             ENUM('M','F') NOT NULL,
  data_nascimento       DATETIME      NOT NULL,
  local_nascimento      VARCHAR(200)  NOT NULL,
  bi_pai                VARCHAR(20)   NULL,
  nome_pai              VARCHAR(200)  NULL,
  bi_mae                VARCHAR(20)   NOT NULL,
  nome_mae              VARCHAR(200)  NOT NULL,
  nome_completo_crianca VARCHAR(200)  NULL,
  apelidos_crianca      VARCHAR(200)  NULL,
  nome_avo_paterno      VARCHAR(200)  NULL,
  nome_avo_paterna      VARCHAR(200)  NULL,
  nome_avo_materno      VARCHAR(200)  NULL,
  nome_avo_materna      VARCHAR(200)  NULL,
  nome_declarante       VARCHAR(200)  NULL,
  bi_declarante         VARCHAR(20)   NULL,
  contacto_encarregado  VARCHAR(20)   NOT NULL,
  email_encarregado     VARCHAR(200)  NULL,
  tem_whatsapp          BOOLEAN       NOT NULL DEFAULT FALSE,
  estado                ENUM('incompleto','aguarda_aprovacao','aprovado','rejeitado','bi_invalido') NOT NULL DEFAULT 'incompleto',
  motivo_rejeicao       TEXT          NULL,
  criado_em             DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado_em        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (hospital_id) REFERENCES hospitais(id)
);

-- TABELA 4 — REGISTOS PERMANENTES DE NASCIMENTO
CREATE TABLE IF NOT EXISTS registos_nascimento (
  id               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pre_registo_id   INT UNSIGNED  NOT NULL UNIQUE,
  nuic             VARCHAR(20)   NOT NULL UNIQUE,
  nome_completo    VARCHAR(200)  NOT NULL,
  apelidos         VARCHAR(200)  NOT NULL,
  sexo             ENUM('M','F') NOT NULL,
  data_nascimento  DATETIME      NOT NULL,
  local_nascimento VARCHAR(200)  NOT NULL,
  nome_pai         VARCHAR(200)  NULL,
  nome_mae         VARCHAR(200)  NOT NULL,
  nome_avo_paterno VARCHAR(200)  NULL,
  nome_avo_paterna VARCHAR(200)  NULL,
  nome_avo_materno VARCHAR(200)  NULL,
  nome_avo_materna VARCHAR(200)  NULL,
  funcionario_nome VARCHAR(200)  NOT NULL,
  aprovado_em      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  pdf_path         VARCHAR(500)  NULL,
  pdf_enviado      BOOLEAN       NOT NULL DEFAULT FALSE,
  FOREIGN KEY (pre_registo_id) REFERENCES pre_registos_nascimento(id)
);

-- TABELA 5 — PRÉ-REGISTOS DE ÓBITO
CREATE TABLE IF NOT EXISTS pre_registos_obito (
  id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  hospital_id         INT UNSIGNED NOT NULL,
  referencia_hospital VARCHAR(100) NOT NULL,
  bi_falecido         VARCHAR(20)  NOT NULL,
  nome_falecido       VARCHAR(200) NOT NULL,
  data_obito          DATETIME     NOT NULL,
  local_obito         VARCHAR(200) NOT NULL,
  causa_obito         VARCHAR(500) NULL,
  nome_declarante     VARCHAR(200) NOT NULL,
  bi_declarante       VARCHAR(20)  NOT NULL,
  contacto_declarante VARCHAR(20)  NOT NULL,
  email_declarante    VARCHAR(200) NULL,
  tem_whatsapp        BOOLEAN      NOT NULL DEFAULT FALSE,
  estado              ENUM('aguarda_aprovacao','aprovado','rejeitado','bi_invalido') NOT NULL DEFAULT 'aguarda_aprovacao',
  motivo_rejeicao     TEXT         NULL,
  criado_em           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado_em      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (hospital_id) REFERENCES hospitais(id)
);

-- TABELA 6 — REGISTOS PERMANENTES DE ÓBITO
CREATE TABLE IF NOT EXISTS registos_obito (
  id               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pre_registo_id   INT UNSIGNED NOT NULL UNIQUE,
  nuic_obito       VARCHAR(20)  NOT NULL UNIQUE,
  nome_falecido    VARCHAR(200) NOT NULL,
  bi_falecido      VARCHAR(20)  NOT NULL,
  data_obito       DATETIME     NOT NULL,
  local_obito      VARCHAR(200) NOT NULL,
  causa_obito      VARCHAR(500) NULL,
  nome_declarante  VARCHAR(200) NOT NULL,
  funcionario_nome VARCHAR(200) NOT NULL,
  aprovado_em      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  pdf_path         VARCHAR(500) NULL,
  pdf_enviado      BOOLEAN      NOT NULL DEFAULT FALSE,
  FOREIGN KEY (pre_registo_id) REFERENCES pre_registos_obito(id)
);

-- TABELA 7 — LOG DE NOTIFICAÇÕES
CREATE TABLE IF NOT EXISTS notificacoes_log (
  id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tipo_registo   ENUM('nascimento','obito') NOT NULL,
  pre_registo_id INT UNSIGNED NOT NULL,
  canal          ENUM('whatsapp','email','pendente') NOT NULL,
  destinatario   VARCHAR(200) NOT NULL,
  mensagem       TEXT         NOT NULL,
  com_pdf        BOOLEAN      NOT NULL DEFAULT FALSE,
  estado_envio   ENUM('enviado','falhou','pendente') NOT NULL DEFAULT 'pendente',
  erro_detalhe   TEXT         NULL,
  enviado_em     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- TABELA 8 — CONFIGURAÇÕES DO SISTEMA
CREATE TABLE IF NOT EXISTS configuracoes (
  chave    VARCHAR(100) PRIMARY KEY,
  valor    VARCHAR(500) NOT NULL,
  descricao VARCHAR(500) NULL
);

INSERT INTO configuracoes (chave, valor, descricao) VALUES
  ('intervalo_notificacao_dias', '15',                         'Intervalo de reenvio em dias (usar 0.001 para testes)'),
  ('nome_conservatoria',         'Conservatória do Registo Civil de Beira', 'Nome oficial nos documentos PDF'),
  ('cidade_conservatoria',       'Beira',                      'Cidade da conservatória'),
  ('provincia_conservatoria',    'Sofala',                     'Província da conservatória'),
  ('email_remetente',            'registocivil@exemplo.co.mz', 'Email para envio de notificações'),
  ('nuic_prefixo_nasc',          'NASC',                       'Prefixo do NUIC para nascimentos'),
  ('nuic_prefixo_obit',          'OBIT',                       'Prefixo do NUIC para óbitos'); 
