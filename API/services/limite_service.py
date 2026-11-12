from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.limite import Limite
from models.categoria import Categoria
from schemas.limite import LimiteRequest


def _validar_categoria_do_usuario(db: Session, usu_id: int, cat_id: int) -> Categoria:
    categoria = db.query(Categoria).filter(
        Categoria.cat_id == cat_id, Categoria.usu_id == usu_id
    ).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return categoria


def listar_limites(db: Session, usu_id: int):
    return (
        db.query(Limite)
        .join(Categoria, Limite.cat_id == Categoria.cat_id)
        .filter(Categoria.usu_id == usu_id)
        .all()
    )


def definir_limite(db: Session, usu_id: int, dados: LimiteRequest) -> Limite:
    _validar_categoria_do_usuario(db, usu_id, dados.cat_id)

    limite = db.query(Limite).filter(Limite.cat_id == dados.cat_id).first()
    if limite is None:
        limite = Limite(cat_id=dados.cat_id, lim_valor=dados.valor)
        db.add(limite)
    else:
        limite.lim_valor = dados.valor

    db.commit()
    db.refresh(limite)
    return limite


def deletar_limite(db: Session, usu_id: int, lim_id: int) -> None:
    limite = (
        db.query(Limite)
        .join(Categoria, Limite.cat_id == Categoria.cat_id)
        .filter(Limite.lim_id == lim_id, Categoria.usu_id == usu_id)
        .first()
    )
    if limite is None:
        raise HTTPException(status_code=404, detail="Limite não encontrado.")
    db.delete(limite)
    db.commit()
