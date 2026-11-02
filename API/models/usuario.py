from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Usuario(Base):
    __tablename__ = "t_usuario"

    usu_id: Mapped[int] = mapped_column(primary_key=True)
    usu_login: Mapped[str] = mapped_column(String(50), unique=True)
    usu_nome: Mapped[str] = mapped_column(String(100))
    usu_email: Mapped[str] = mapped_column(String(255), unique=True)
    usu_senha: Mapped[str] = mapped_column(String(255))
    usu_status: Mapped[str] = mapped_column(String(1), server_default="A")
    data_cadastro: Mapped[datetime] = mapped_column(server_default=func.now()
    data_nascimento: Mapped[date] = mapped_column())