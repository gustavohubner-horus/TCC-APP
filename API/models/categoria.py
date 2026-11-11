from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Categoria(Base):
    __tablename__ = "t_categoria"

    cat_id: Mapped[int] = mapped_column(primary_key=True)
    usu_id: Mapped[int] = mapped_column(ForeignKey("t_usuario.usu_id"))
    cat_nome: Mapped[str] = mapped_column(String(100))
    data_cadastro: Mapped[datetime] = mapped_column(server_default=func.now())
