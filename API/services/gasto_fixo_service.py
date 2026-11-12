import calendar
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.gasto_fixo import GastoFixo
from models.gasto import Gasto
from models.categoria import Categoria
from schemas.gasto_fixo import GastoFixoRequest
from services.grupo_service import obter_grupo_pessoal


def _validar_categoria(db: Session, usu_id: int, cat_id):
    if cat_id is None:
        return
    categoria = db.query(Categoria).filter(
        Categoria.cat_id == cat_id, Categoria.usu_id == usu_id
    ).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")


def listar_gastos_fixos(db: Session, usu_id: int):
    return db.query(GastoFixo).filter(GastoFixo.usu_id == usu_id).all()


def buscar_gasto_fixo(db: Session, usu_id: int, gfx_id: int) -> GastoFixo:
    fixo = db.query(GastoFixo).filter(
        GastoFixo.gfx_id == gfx_id, GastoFixo.usu_id == usu_id
    ).first()
    if fixo is None:
        raise HTTPException(status_code=404, detail="Gasto fixo não encontrado.")
    return fixo


def criar_gasto_fixo(db: Session, usu_id: int, dados: GastoFixoRequest) -> GastoFixo:
    _validar_categoria(db, usu_id, dados.cat_id)
    fixo = GastoFixo(
        usu_id=usu_id,
        cat_id=dados.cat_id,
        gfx_descricao=dados.descricao.strip(),
        gfx_valor=dados.valor,
        gfx_dia=dados.dia,
        gfx_ativo=dados.ativo,
    )
    db.add(fixo)
    db.commit()
    db.refresh(fixo)
    return fixo


def atualizar_gasto_fixo(db: Session, usu_id: int, gfx_id: int, dados: GastoFixoRequest) -> GastoFixo:
    fixo = buscar_gasto_fixo(db, usu_id, gfx_id)
    _validar_categoria(db, usu_id, dados.cat_id)
    fixo.gfx_descricao = dados.descricao.strip()
    fixo.gfx_valor = dados.valor
    fixo.gfx_dia = dados.dia
    fixo.cat_id = dados.cat_id
    fixo.gfx_ativo = dados.ativo
    db.commit()
    db.refresh(fixo)
    return fixo


def deletar_gasto_fixo(db: Session, usu_id: int, gfx_id: int) -> None:
    fixo = buscar_gasto_fixo(db, usu_id, gfx_id)
    db.delete(fixo)
    db.commit()


def processar_mes(db: Session, usu_id: int) -> None:
    hoje = date.today()
    primeiro_dia = date(hoje.year, hoje.month, 1)
    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
    grupo = obter_grupo_pessoal(db, usu_id)

    fixos = db.query(GastoFixo).filter(
        GastoFixo.usu_id == usu_id, GastoFixo.gfx_ativo == True
    ).all()

    for fixo in fixos:
        existe = db.query(Gasto).filter(
            Gasto.gfx_id == fixo.gfx_id, Gasto.gas_data >= primeiro_dia
        ).first()
        if existe:
            continue
        dia = min(fixo.gfx_dia, ultimo_dia)
        gasto = Gasto(
            usu_id=usu_id,
            gru_id=grupo.gru_id,
            cat_id=fixo.cat_id,
            gfx_id=fixo.gfx_id,
            gas_descricao=fixo.gfx_descricao,
            gas_valor=fixo.gfx_valor,
            gas_data=date(hoje.year, hoje.month, dia),
        )
        db.add(gasto)

    db.commit()
