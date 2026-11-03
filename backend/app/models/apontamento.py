import uuid
from datetime import date, datetime, time

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Apontamento(Base):
    __tablename__ = "apontamentos"
    __table_args__ = (
        UniqueConstraint(
            "funcionario_id", "data", name="uq_apontamento_funcionario_data"
        ),
        CheckConstraint(
            "hora_saida > hora_entrada", name="ck_apontamento_saida_depois_entrada"
        ),
        CheckConstraint(
            "(saida_almoco IS NULL) = (volta_almoco IS NULL)",
            name="ck_apontamento_almoco_completo",
        ),
        CheckConstraint(
            "saida_almoco IS NULL OR ((hora_entrada < saida_almoco) AND (saida_almoco < volta_almoco) AND (volta_almoco < hora_saida))",
            name="ck_apontamento_ordem_almoco",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    funcionario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("funcionarios.id", ondelete="RESTRICT")
    )
    data: Mapped[date]
    hora_entrada: Mapped[time]
    saida_almoco: Mapped[time | None]
    volta_almoco: Mapped[time | None]
    hora_saida: Mapped[time]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
