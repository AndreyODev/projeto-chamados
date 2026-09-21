from fastapi import APIRouter, HTTPException
from controllers.chamados import cadastrar_chamado, consultar_chamado, obter_chamados
from schemas.chamados import ChamadoRequest

router = APIRouter()

@router.get("/chamados")
def listar_chamados():
    return obter_chamados()

@router.post("/chamados", status_code=201)
def criar_chamado(dados: ChamadoRequest):
    return cadastrar_chamado(dados)


@router.get("/chamados/{chamado_id}")
def consultar_por_id(chamado_id: int):
    chamado = consultar_chamado(chamado_id)
    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return chamado