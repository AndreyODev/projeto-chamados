from typing import Literal
from pydantic import BaseModel

class ChamadoRequest(BaseModel):
    titulo: str
    descricao: str
    prioridade: Literal["baixa", "media", "alta"]

class ChamadoResponse(BaseModel):
    id: str
    titulo: str
    descricao: str
    prioridade: Literal["baixa", "media", "alta"]