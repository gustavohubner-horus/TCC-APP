from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.limite import LimiteRequest, LimiteResponse
from services import limite_service
from services.auth_service import get_usuario_logado

router = APIRouter(prefix="/limites", tags=["Limites"])


@router.get("", response_model=list[LimiteResponse])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return limite_service.listar_limites(db, usuario.usu_id)


@router.post("", response_model=LimiteResponse)
def definir(dados: LimiteRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return limite_service.definir_limite(db, usuario.usu_id, dados)


@router.delete("/{lim_id}", status_code=204)
def deletar(lim_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    limite_service.deletar_limite(db, usuario.usu_id, lim_id)
