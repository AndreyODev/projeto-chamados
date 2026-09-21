from fastapi import APIRouter, HTTPException, status
from controllers.chamados import cadastrar_chamado, consultar_chamado, obter_chamados
from schemas.chamados import ChamadoRequest, ChamadoResponse, ListChamadosResponse

router = APIRouter()

@router.get("/chamados", status_code=status.HTTP_200_OK, response_model=ListChamadosResponse)
def listar_chamados():
    return obter_chamados()

@router.post("/chamados", status_code=status.HTTP_201_CREATED, response_model=ChamadoResponse)
def criar_chamado(dados: ChamadoRequest):
    return cadastrar_chamado(dados)
@router.get("/chamados/{chamado_id}")
def consultar_por_id(chamado_id: int):
    chamado = consultar_chamado(chamado_id)
    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return chamado
