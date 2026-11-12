from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.gasto import Gasto
from models.categoria import Categoria
from schemas.gasto import GastoRequest
from services.grupo_service import obter_grupo_pessoal, validar_membro


def listar_gastos(db: Session, usu_id: int):
    grupo = obter_grupo_pessoal(db, usu_id)
    return (
        db.query(Gasto)
        .filter(Gasto.gru_id == grupo.gru_id)
        .order_by(Gasto.gas_data.desc(), Gasto.gas_id.desc())
        .all()
    )


def criar_gasto(db: Session, usu_id: int, dados: GastoRequest) -> Gasto:
    if dados.cat_id is not None:
        categoria = db.query(Categoria).filter(
            Categoria.cat_id == dados.cat_id, Categoria.usu_id == usu_id
        ).first()
        if categoria is None:
            raise HTTPException(status_code=404, detail="Categoria não encontrada.")

    if dados.gru_id is not None:
        validar_membro(db, usu_id, dados.gru_id)
        gru_id = dados.gru_id
    else:
        gru_id = obter_grupo_pessoal(db, usu_id).gru_id

    gasto = Gasto(
        usu_id=usu_id,
        gru_id=gru_id,
        cat_id=dados.cat_id,
        gas_descricao=dados.descricao.strip() if dados.descricao else None,
        gas_valor=dados.valor,
        gas_data=dados.data,
    )
    db.add(gasto)
    db.commit()
    db.refresh(gasto)
    return gasto


def deletar_gasto(db: Session, usu_id: int, gas_id: int) -> None:
    gasto = db.query(Gasto).filter(
        Gasto.gas_id == gas_id, Gasto.usu_id == usu_id
    ).first()
    if gasto is None:
        raise HTTPException(status_code=404, detail="Gasto não encontrado.")
    db.delete(gasto)
    db.commit()
