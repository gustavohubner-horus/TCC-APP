CREATE TABLE T_USUARIO (
    USU_ID          SERIAL       PRIMARY KEY,
    USU_LOGIN       VARCHAR(50)  NOT NULL UNIQUE,
    USU_NOME        VARCHAR(100) NOT NULL,
    USU_EMAIL       VARCHAR(255) NOT NULL UNIQUE,
    USU_SENHA       VARCHAR(255) NOT NULL,                -- hash da senha
    USU_STATUS      VARCHAR(1)   NOT NULL DEFAULT 'A',  -- A = ativo, I = inativo
    DATA_CADASTRO   TIMESTAMP    NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE T_USUARIO IS 'Usuários cadastrados';

COMMENT ON COLUMN T_USUARIO.USU_ID        IS 'ID do usuário';
COMMENT ON COLUMN T_USUARIO.USU_LOGIN     IS 'login do usuário';
COMMENT ON COLUMN T_USUARIO.USU_NOME      IS 'Nome completo do usuário';
COMMENT ON COLUMN T_USUARIO.USU_EMAIL     IS 'E-mail de login';
COMMENT ON COLUMN T_USUARIO.USU_SENHA     IS 'Hash da senha (nunca a senha em texto)';
COMMENT ON COLUMN T_USUARIO.USU_STATUS    IS 'Situação do usuário: A = ativo, I = inativo';
COMMENT ON COLUMN T_USUARIO.DATA_CADASTRO IS 'Data e hora do cadastro';