from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.categoria import Categoria
from schemas.categoria import CategoriaRequest


def listar_categorias(db: Session, usu_id: int):
    return db.query(Categoria).filter(Categoria.usu_id == usu_id).all()


def buscar_categoria(db: Session, usu_id: int, cat_id: int) -> Categoria:
    categoria = db.query(Categoria).filter(
        Categoria.cat_id == cat_id, Categoria.usu_id == usu_id
    ).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return categoria


def criar_categoria(db: Session, usu_id: int, dados: CategoriaRequest) -> Categoria:
    categoria = Categoria(usu_id=usu_id, cat_nome=dados.nome.strip())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def atualizar_categoria(db: Session, usu_id: int, cat_id: int, dados: CategoriaRequest) -> Categoria:
    categoria = buscar_categoria(db, usu_id, cat_id)
    categoria.cat_nome = dados.nome.strip()
    db.commit()
    db.refresh(categoria)
    return categoria


def deletar_categoria(db: Session, usu_id: int, cat_id: int) -> None:
    categoria = buscar_categoria(db, usu_id, cat_id)
    db.delete(categoria)
    db.commit()
