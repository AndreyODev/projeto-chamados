from backend.repositories.chamados import chamados, salvar_chamado
from backend.schemas.chamados import ChamadoRequest

def listar_chamados():
    return chamados

def criar_chamado(dados: ChamadoRequest):
    chamado = {
        "id": str(len(chamados) + 1),
        "titulo": dados.titulo,
        "descricao": dados.descricao,
        "prioridade": dados.prioridade,
    }
    return salvar_chamado(chamado)