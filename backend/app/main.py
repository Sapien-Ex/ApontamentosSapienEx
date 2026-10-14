from fastapi import FastAPI

from app.api.routes import clientes, health
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(clientes.router)
