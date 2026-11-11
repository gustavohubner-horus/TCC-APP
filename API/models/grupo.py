from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Grupo(Base):
    __tablename__ = "t_grupo"

    gru_id: Mapped[int] = mapped_column(primary_key=True)
    usu_id: Mapped[int] = mapped_column(ForeignKey("t_usuario.usu_id"))
    gru_nome: Mapped[str] = mapped_column(String(100))
    gru_tipo: Mapped[str] = mapped_column(String(1), server_default="P")
    data_criacao: Mapped[datetime] = mapped_column(server_default=func.now())
