from repositories.chamados import buscar_chamado, listar_chamados as buscar_chamados
from repositories.chamados import salvar_chamado
from schemas.chamados import ChamadoRequest


def listar_chamados() -> dict:
    chamados = buscar_chamados()
    return {
        "chamados": chamados,
        "tamanho": len(chamados),
    }


def obter_chamado(chamado_id: int):
    return buscar_chamado(chamado_id)


def criar_chamado(dados: ChamadoRequest):
    return salvar_chamado(
        {
            "titulo": dados.titulo,
            "descricao": dados.descricao,
            "prioridade": dados.prioridade,
            "status": dados.status,
        }
    )
