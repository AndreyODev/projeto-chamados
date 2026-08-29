from fastapi import FastAPI
from backend.routes.chamados import router as chamados_router

app = FastAPI(
    title="API de Chamados",
    description="API inicial para registro e acompanhamento de chamados de suporte.",
    version="1.0.0",
)

app.include_router(chamados_router)