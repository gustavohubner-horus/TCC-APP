from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.grupo import (
    GrupoRequest,
    GrupoResponse,
    MembroRequest,
    MembroResponse,
    FechamentoItem,
)
from schemas.gasto import GastoResponse
from services import grupo_service
from services.auth_service import get_usuario_logado

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.get("", response_model=list[GrupoResponse])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.listar_grupos(db, usuario.usu_id)


@router.post("", response_model=GrupoResponse, status_code=201)
def criar(dados: GrupoRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.criar_grupo(db, usuario.usu_id, dados.nome)


@router.get("/{gru_id}", response_model=GrupoResponse)
def buscar(gru_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.buscar_grupo(db, usuario.usu_id, gru_id)


@router.get("/{gru_id}/membros", response_model=list[MembroResponse])
def listar_membros(gru_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.listar_membros(db, usuario.usu_id, gru_id)


@router.post("/{gru_id}/membros", response_model=MembroResponse, status_code=201)
def adicionar_membro(gru_id: int, dados: MembroRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.adicionar_membro(db, usuario.usu_id, gru_id, dados.login)


@router.delete("/{gru_id}/membros/{membro_id}", status_code=204)
def remover_membro(gru_id: int, membro_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    grupo_service.remover_membro(db, usuario.usu_id, gru_id, membro_id)


@router.get("/{gru_id}/gastos", response_model=list[GastoResponse])
def listar_gastos(gru_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.listar_gastos_grupo(db, usuario.usu_id, gru_id)


@router.get("/{gru_id}/fechamento", response_model=list[FechamentoItem])
def fechamento(gru_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return grupo_service.fechamento(db, usuario.usu_id, gru_id)
