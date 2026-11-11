from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class GastoFixoRequest(BaseModel):
    descricao: str = Field(min_length=1, max_length=255)
    valor: Decimal = Field(gt=0)
    dia: int = Field(ge=1, le=31)
    cat_id: Optional[int] = None
    ativo: bool = True


class GastoFixoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    gfx_id: int
    usu_id: int
    cat_id: Optional[int]
    gfx_descricao: str
    gfx_valor: Decimal
    gfx_dia: int
    gfx_ativo: bool
