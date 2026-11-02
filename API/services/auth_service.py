from fastapi import HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioEntrada

password_hash = PasswordHash.recommended()

def cadastrar_usuario(db: Session, dados: UsuarioEntrada) -> Usuario:
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