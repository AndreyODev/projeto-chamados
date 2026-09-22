from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field


class ChamadoRequest(BaseModel):
    titulo: str = Field(min_length=1)
    descricao: str = Field(min_length=1)
    prioridade: Literal["baixa", "media", "alta"]
    status: Literal["aberto", "em_andamento", "fechado"] = "aberto"


class ChamadoResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    prioridade: Literal["baixa", "media", "alta"]
    status: Literal["aberto", "em_andamento", "fechado"]
    criado_em: datetime


class ListChamadosResponse(BaseModel):
    chamados: list[ChamadoResponse]
    tamanho: int
