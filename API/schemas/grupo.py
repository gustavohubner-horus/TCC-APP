from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class GrupoRequest(BaseModel):
    nome: str = Field(min_length=1, max_length=100)


class GrupoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    gru_id: int
    usu_id: int
    gru_nome: str
    gru_tipo: str
    data_criacao: datetime


class MembroRequest(BaseModel):
    login: str


class MembroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usu_id: int
    usu_nome: str
    usu_login: str


class FechamentoItem(BaseModel):
    usu_id: int
    nome: str
    pago: Decimal
    cota: Decimal
    saldo: Decimal
