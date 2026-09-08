from fastapi import APIRouter
from backend.controllers.chamados import obter_chamados, cadastrar_chamado
from backend.schemas.chamados import ChamadoRequest

router = APIRouter()

@router.get("/chamados")
def listar_chamados():
    return obter_chamados()

@router.post("/chamados", status_code=201)
def criar_chamado(dados: ChamadoRequest):
    return cadastrar_chamado(dados)