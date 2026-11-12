from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.grupo import Grupo
from models.participante import Participante
from models.usuario import Usuario
from models.gasto import Gasto


def obter_grupo_pessoal(db: Session, usu_id: int) -> Grupo:
    grupo = db.query(Grupo).filter(
        Grupo.usu_id == usu_id, Grupo.gru_tipo == "P"
    ).first()

    if grupo is None:
        grupo = Grupo(usu_id=usu_id, gru_nome="Pessoal", gru_tipo="P")
        db.add(grupo)
        db.commit()
        db.refresh(grupo)

    return grupo


def validar_membro(db: Session, usu_id: int, gru_id: int) -> None:
    participante = db.query(Participante).filter(
        Participante.gru_id == gru_id, Participante.usu_id == usu_id
    ).first()
    if participante is None:
        raise HTTPException(status_code=403, detail="Você não participa deste grupo.")


def _validar_dono(db: Session, usu_id: int, gru_id: int) -> Grupo:
    grupo = db.query(Grupo).filter(Grupo.gru_id == gru_id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")
    if grupo.usu_id != usu_id:
        raise HTTPException(status_code=403, detail="Apenas o dono pode gerenciar o grupo.")
    return grupo


def listar_grupos(db: Session, usu_id: int):
    return (
        db.query(Grupo)
        .join(Participante, Participante.gru_id == Grupo.gru_id)
        .filter(Participante.usu_id == usu_id, Grupo.gru_tipo == "C")
        .all()
    )


def criar_grupo(db: Session, usu_id: int, nome: str) -> Grupo:
    grupo = Grupo(usu_id=usu_id, gru_nome=nome.strip(), gru_tipo="C")
    db.add(grupo)
    db.commit()
    db.refresh(grupo)

    db.add(Participante(gru_id=grupo.gru_id, usu_id=usu_id))
    db.commit()
    return grupo


def buscar_grupo(db: Session, usu_id: int, gru_id: int) -> Grupo:
    validar_membro(db, usu_id, gru_id)
    grupo = db.query(Grupo).filter(Grupo.gru_id == gru_id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")
    return grupo


def listar_membros(db: Session, usu_id: int, gru_id: int):
    validar_membro(db, usu_id, gru_id)
    return (
        db.query(Usuario)
        .join(Participante, Participante.usu_id == Usuario.usu_id)
        .filter(Participante.gru_id == gru_id)
        .all()
    )


def adicionar_membro(db: Session, usu_id: int, gru_id: int, login: str) -> Usuario:
    _validar_dono(db, usu_id, gru_id)
    novo = db.query(Usuario).filter(Usuario.usu_login == login.lower()).first()
    if novo is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    ja_participa = db.query(Participante).filter(
        Participante.gru_id == gru_id, Participante.usu_id == novo.usu_id
    ).first()
    if ja_participa:
        raise HTTPException(status_code=409, detail="Este usuário já está no grupo.")

    db.add(Participante(gru_id=gru_id, usu_id=novo.usu_id))
    db.commit()
    return novo


def remover_membro(db: Session, usu_id: int, gru_id: int, membro_id: int) -> None:
    grupo = _validar_dono(db, usu_id, gru_id)
    if membro_id == grupo.usu_id:
        raise HTTPException(status_code=400, detail="O dono não pode sair do grupo.")

    participante = db.query(Participante).filter(
        Participante.gru_id == gru_id, Participante.usu_id == membro_id
    ).first()
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")

    db.delete(participante)
    db.commit()


def listar_gastos_grupo(db: Session, usu_id: int, gru_id: int):
    validar_membro(db, usu_id, gru_id)
    return (
        db.query(Gasto)
        .filter(Gasto.gru_id == gru_id)
        .order_by(Gasto.gas_data.desc(), Gasto.gas_id.desc())
        .all()
    )


def fechamento(db: Session, usu_id: int, gru_id: int):
    validar_membro(db, usu_id, gru_id)
    membros = listar_membros(db, usu_id, gru_id)
    gastos = db.query(Gasto).filter(Gasto.gru_id == gru_id).all()

    total = sum((g.gas_valor for g in gastos), 0)
    quantidade = len(membros)
    cota = total / quantidade if quantidade else 0

    resultado = []
    for membro in membros:
        pago = sum((g.gas_valor for g in gastos if g.usu_id == membro.usu_id), 0)
        resultado.append({
            "usu_id": membro.usu_id,
            "nome": membro.usu_nome,
            "pago": pago,
            "cota": cota,
            "saldo": pago - cota,
        })
    return resultado
