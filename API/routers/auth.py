from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.usuario import (
    UsuarioRequest,
    UsuarioResponse,
    Login,
    TokenLogin,
    AlterarSenha,
)
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/cadastro", response_model=UsuarioResponse, status_code=201)
def cadastrar(dados: UsuarioRequest, db: Session = Depends(get_db)):
    return auth_service.cadastrar_usuario(db, dados)


@router.post("/login", response_model=TokenLogin)
def login(dados: Login, db: Session = Depends(get_db)):
    return auth_service.validar_login(db, dados)


@router.put("/senha", status_code=204)
def alterar_senha(
    dados: AlterarSenha,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(auth_service.get_usuario_logado),
):
    auth_service.alterar_senha(db, usuario, dados.senha_atual, dados.senha_nova)
