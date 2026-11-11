from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Gasto(Base):
    __tablename__ = "t_gasto"

    gas_id: Mapped[int] = mapped_column(primary_key=True)
    usu_id: Mapped[int] = mapped_column(ForeignKey("t_usuario.usu_id"))
    gru_id: Mapped[int] = mapped_column(ForeignKey("t_grupo.gru_id"))
    cat_id: Mapped[Optional[int]] = mapped_column(ForeignKey("t_categoria.cat_id"))
    gfx_id: Mapped[Optional[int]] = mapped_column(ForeignKey("t_gasto_fixo.gfx_id"))
    gas_descricao: Mapped[Optional[str]] = mapped_column(String(255))
    gas_valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    gas_data: Mapped[date] = mapped_column(Date)
    data_cadastro: Mapped[datetime] = mapped_column(server_default=func.now())
