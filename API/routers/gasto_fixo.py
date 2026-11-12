from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.gasto_fixo import GastoFixoRequest, GastoFixoResponse
from services import gasto_fixo_service
from services.auth_service import get_usuario_logado

router = APIRouter(prefix="/gastos-fixos", tags=["Gastos fixos"])


@router.get("", response_model=list[GastoFixoResponse])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return gasto_fixo_service.listar_gastos_fixos(db, usuario.usu_id)


@router.post("", response_model=GastoFixoResponse, status_code=201)
def criar(dados: GastoFixoRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return gasto_fixo_service.criar_gasto_fixo(db, usuario.usu_id, dados)


@router.put("/{gfx_id}", response_model=GastoFixoResponse)
def atualizar(gfx_id: int, dados: GastoFixoRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return gasto_fixo_service.atualizar_gasto_fixo(db, usuario.usu_id, gfx_id, dados)


@router.delete("/{gfx_id}", status_code=204)
def deletar(gfx_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    gasto_fixo_service.deletar_gasto_fixo(db, usuario.usu_id, gfx_id)


@router.post("/processar", status_code=204)
def processar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    gasto_fixo_service.processar_mes(db, usuario.usu_id)
