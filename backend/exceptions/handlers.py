from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _campo(localizacao: tuple[object, ...]) -> str:
    return str(localizacao[-1]) if localizacao else "geral"


def _mensagem_erro(erro: dict, campo: str) -> str:
    tipo = erro.get("type")

    if tipo == "missing":
        mensagens = {
            "titulo": "O título é obrigatório.",
            "descricao": "A descrição é obrigatória.",
            "prioridade": "A prioridade é obrigatória.",
        }
        return mensagens.get(campo, "Este campo é obrigatório.")

    if campo == "prioridade":
        return "Use baixa, media ou alta."

    if tipo == "string_too_short":
        return "Informe um valor com pelo menos 1 caractere."

    if tipo == "int_parsing":
        return "Informe um número inteiro válido."

    return "Valor inválido."


async def tratar_validacao(request: Request, exc: RequestValidationError):
    detalhes = []
    for erro in exc.errors():
        campo = _campo(tuple(erro.get("loc", ())))
        detalhes.append(
            {
                "campo": campo,
                "mensagem": _mensagem_erro(erro, campo),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"erro": "Dado inválido", "detalhes": detalhes},
    )


async def tratar_http_exception(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "erro": "Recurso não encontrado",
                "detalhes": [
                    {
                        "campo": "id",
                        "mensagem": "Não existe chamado com o id informado.",
                    }
                ],
            },
        )

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})