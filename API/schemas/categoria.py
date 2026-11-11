from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CategoriaRequest(BaseModel):
    nome: str = Field(min_length=1, max_length=100)


class CategoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cat_id: int
    usu_id: int
    cat_nome: str
    data_cadastro: datetime
