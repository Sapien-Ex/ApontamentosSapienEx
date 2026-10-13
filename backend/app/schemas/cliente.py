from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClienteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    razao_social: str = Field(min_length=1, max_length=150)
    nome_fantasia: str = Field(min_length=1, max_length=100)
    cnpj: str | None = Field(default=None, min_length=14, max_length=14)


class ClienteUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    razao_social: str | None = Field(default=None, min_length=1, max_length=150)
    nome_fantasia: str | None = Field(default=None, min_length=1, max_length=100)
    cnpj: str | None = Field(default=None, min_length=14, max_length=14)


class ClienteRead(BaseModel):
    id: UUID
    razao_social: str
    nome_fantasia: str
    cnpj: str | None
    ativo: bool
    created_at: datetime
