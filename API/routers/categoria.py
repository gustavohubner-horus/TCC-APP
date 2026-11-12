from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.categoria import CategoriaRequest, CategoriaResponse
from services import categoria_service
from services.auth_service import get_usuario_logado

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("", response_model=list[CategoriaResponse])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return categoria_service.listar_categorias(db, usuario.usu_id)


@router.get("/{cat_id}", response_model=CategoriaResponse)
def buscar(cat_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return categoria_service.buscar_categoria(db, usuario.usu_id, cat_id)


@router.post("", response_model=CategoriaResponse, status_code=201)
def criar(dados: CategoriaRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return categoria_service.criar_categoria(db, usuario.usu_id, dados)


@router.put("/{cat_id}", response_model=CategoriaResponse)
def atualizar(cat_id: int, dados: CategoriaRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    return categoria_service.atualizar_categoria(db, usuario.usu_id, cat_id, dados)


@router.delete("/{cat_id}", status_code=204)
def deletar(cat_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_logado)):
    categoria_service.deletar_categoria(db, usuario.usu_id, cat_id)
