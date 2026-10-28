from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class Registro(BaseModel):
    descricao: str = Field(description="Resumo curto do que foi registrado")
    valor: Optional[float] = Field(None, description="Valor em reais, se houver")
    local: Optional[str] = Field(None, description="Nome do estabelecimento ou lugar onde foi gasto, se houver")
    data: Optional[date] = Field(None, description="Data no formato AAAA-MM-DD, se houver")