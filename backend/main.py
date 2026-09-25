from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from backend.routes.chamados import router as chamados_router
from backend.exceptions.handlers import tratar_http_exception, tratar_validacao

app = FastAPI(
    title="API de Chamados",
    description="API inicial para registro e acompanhamento de chamados de suporte.",
    version="1.0.0",
)

app.add_exception_handler(RequestValidationError, tratar_validacao)
app.add_exception_handler(HTTPException, tratar_http_exception)

app.include_router(chamados_router)