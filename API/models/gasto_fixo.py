from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class GastoFixo(Base):
    __tablename__ = "t_gasto_fixo"

    gfx_id: Mapped[int] = mapped_column(primary_key=True)
    usu_id: Mapped[int] = mapped_column(ForeignKey("t_usuario.usu_id"))
    cat_id: Mapped[Optional[int]] = mapped_column(ForeignKey("t_categoria.cat_id"))
    gfx_descricao: Mapped[str] = mapped_column(String(255))
    gfx_valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    gfx_dia: Mapped[int] = mapped_column(Integer)
    gfx_ativo: Mapped[bool] = mapped_column(Boolean, server_default="true")
