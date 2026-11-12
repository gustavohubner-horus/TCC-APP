from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.gasto import GastoRequest, GastoResponse
from services import gasto_service
from services.auth_service import get_usuario_logado

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.get("", response_model=list[GastoResponse])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return gasto_service.listar_gastos(db, usuario.usu_id)


@router.post("", response_model=GastoResponse, status_code=201)
def criar(dados: GastoRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return gasto_service.criar_gasto(db, usuario.usu_id, dados)


@router.delete("/{gas_id}", status_code=204)
def deletar(gas_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    gasto_service.deletar_gasto(db, usuario.usu_id, gas_id)
