from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Participante(Base):
    __tablename__ = "t_participante"

    par_id: Mapped[int] = mapped_column(primary_key=True)
    gru_id: Mapped[int] = mapped_column(ForeignKey("t_grupo.gru_id"))
    usu_id: Mapped[int] = mapped_column(ForeignKey("t_usuario.usu_id"))
