import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.funcionario import Nivel


class FuncionarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=1, max_length=150)
    nivel: Nivel


class FuncionarioUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str | None = Field(default=None, min_length=1, max_length=150)
    nivel: Nivel | None = None


class FuncionarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    nivel: Nivel
    ativo: bool
    created_at: datetime
