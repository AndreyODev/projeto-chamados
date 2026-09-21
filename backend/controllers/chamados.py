from schemas.chamados import ChamadoRequest
from services.chamados import listar_chamados, criar_chamado

def obter_chamados():
    return listar_chamados()

def cadastrar_chamado(dados: ChamadoRequest):
    return criar_chamado(dados)
