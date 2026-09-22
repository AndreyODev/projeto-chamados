from backend.schemas.chamados import ChamadoRequest
from backend.services.chamados import criar_chamado, listar_chamados, obter_chamado

def obter_chamados():
    return listar_chamados()

def cadastrar_chamado(dados: ChamadoRequest):
    return criar_chamado(dados)

def consultar_chamado(chamado_id: int):
    return obter_chamado(chamado_id)
