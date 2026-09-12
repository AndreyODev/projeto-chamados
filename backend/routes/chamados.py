from fastapi import APIRouter, status
from controllers.chamados import obter_chamados, cadastrar_chamado
from schemas.chamados import ChamadoRequest, ChamadoResponse, ListChamadosResponse

router = APIRouter()

@router.get("/chamados", status_code=status.HTTP_200_OK, response_model=ListChamadosResponse)
def listar_chamados():
    return obter_chamados()

@router.post("/chamados", status_code=status.HTTP_201_CREATED, response_model=ChamadoResponse)
def criar_chamado(dados: ChamadoRequest):
    return cadastrar_chamado(dados)
