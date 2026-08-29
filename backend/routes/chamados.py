from fastapi import APIRouter
from backend.controllers.chamados import obter_chamados

router = APIRouter()

@router.get("/chamados")
def listar_chamados():
    return obter_chamados()