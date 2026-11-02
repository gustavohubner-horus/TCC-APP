from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioEntrada(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8)
    data_nascimento: date
    login: str = Field(min_length=3, max_length=50)


class UsuarioSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usu_id: int
    usu_login: str
    usu_nome: str
    usu_email: str
    usu_status: str
    data_cadastro: datetime
    data_nascimento: date