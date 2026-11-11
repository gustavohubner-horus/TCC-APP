from decimal import Decimal
from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Limite(Base):
    __tablename__ = "t_limite"

    lim_id: Mapped[int] = mapped_column(primary_key=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey("t_categoria.cat_id"), unique=True)
    lim_valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
