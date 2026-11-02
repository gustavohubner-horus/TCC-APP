from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario import UsuarioEntrada, UsuarioSaida
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/cadastro", response_model=UsuarioSaida, status_code=201)
def cadastrar(dados: UsuarioEntrada, db: Session = Depends(get_db)):
    return auth_service.cadastrar_usuario(db, dados)