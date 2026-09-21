from repositories.chamados import chamados, salvar_chamado
from schemas.chamados import ChamadoRequest
from exceptions.exceptions import InternalServerError

def listar_chamados() -> dict:
    return {
        "chamados": chamados,
        "tamanho": len(chamados)
    }

def criar_chamado(dados: ChamadoRequest) -> dict:
    try:
        chamado = {
            "id": str(len(chamados) + 1),
            "titulo": dados.titulo,
            "descricao": dados.descricao,
            "prioridade": dados.prioridade,
        }
        return salvar_chamado(chamado)
    except Exception as e:
        print("error", e)
        raise InternalServerError()
    