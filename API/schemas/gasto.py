from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GastoRequest(BaseModel):
    descricao: Optional[str] = Field(default=None, max_length=255)
    valor: Decimal = Field(gt=0)
    data: date
    cat_id: Optional[int] = None
    gru_id: Optional[int] = None


class GastoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    gas_id: int
    usu_id: int
    gru_id: int
    cat_id: Optional[int]
    gas_descricao: Optional[str]
    gas_valor: Decimal
    gas_data: date
    data_cadastro: datetime
