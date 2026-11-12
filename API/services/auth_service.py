from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioRequest, Login
from datetime import datetime, timedelta, timezone
import os 
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_db

password_hash = PasswordHash.recommended()
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITMO = "HS256"
JWT_EXPIRA = 7 # Em quantos dias o token expira

def cadastrar_usuario(db: Session, dados: UsuarioRequest) -> Usuario:
    email = dados.email.lower()
    login = dados.login.lower()

    if db.query(Usuario).filter(Usuario.usu_email == email).first():
        raise HTTPException(status_code=409, detail="Este e-mail já está cadastrado.")
    if db.query(Usuario).filter(Usuario.usu_login == login).first():
        raise HTTPException(status_code=409, detail="Este login já está em uso.")

    usuario = Usuario(
        usu_nome=dados.nome.strip(),
        usu_email=email,
        usu_login=login,
        usu_senha=password_hash.hash(dados.senha),
        data_nascimento=dados.data_nascimento,)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def gerar_token(usu_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRA)
    dados_token = {"sub": str(usu_id), "exp": expira}
    return jwt.encode(dados_token, JWT_SECRET, algorithm=JWT_ALGORITMO)


def validar_login(db: Session, dados: Login) -> dict:
    usuario = db.query(Usuario).filter(Usuario.usu_login == dados.login.lower()).first()

    if usuario is None or not password_hash.verify(dados.senha, usuario.usu_senha):
        raise HTTPException(status_code=401, detail="Login ou senha inválidos.")
    if usuario.usu_status != "A":
        raise HTTPException(status_code=403, detail="Usuário inativo.")

    return {"access_token": gerar_token(usuario.usu_id), "usuario": usuario}

seguranca = HTTPBearer()

def get_usuario_logado(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca),
    db: Session = Depends(get_db),
) -> Usuario:
    token = credenciais.credentials
    try:
        dados = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITMO])
        usu_id = int(dados["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sessão expirada. Faça login novamente.")
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido.")

    usuario = db.query(Usuario).filter(Usuario.usu_id == usu_id).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    return usuario


def alterar_senha(db: Session, usuario: Usuario, senha_atual: str, senha_nova: str) -> None:
    if not password_hash.verify(senha_atual, usuario.usu_senha):
        raise HTTPException(status_code=400, detail="Senha atual incorreta.")
    usuario.usu_senha = password_hash.hash(senha_nova)
    db.commit()