from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class LimiteRequest(BaseModel):
    cat_id: int
    valor: Decimal = Field(gt=0)


class LimiteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lim_id: int
    cat_id: int
    lim_valor: Decimal
