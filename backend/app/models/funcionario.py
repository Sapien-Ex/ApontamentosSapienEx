import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Nivel(StrEnum):
    ESTAGIARIO = "ESTAGIÁRIO"
    JUNIOR = "JÚNIOR"
    PLENO = "PLENO"
    SENIOR = "SÊNIOR"


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(150))
    nivel: Mapped[Nivel] = mapped_column(Enum(Nivel, name="nivel_enum"))
    ativo: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
