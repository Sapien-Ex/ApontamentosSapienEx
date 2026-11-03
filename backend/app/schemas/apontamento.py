import uuid
from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field, model_validator

from app.services.calculo_horas import calcular_total_horas, validar_horarios


class ApontamentoCreate(BaseModel):
    funcionario_id: uuid.UUID
    data: date
    hora_entrada: time
    saida_almoco: time | None = None
    volta_almoco: time | None = None
    hora_saida: time

    @model_validator(mode="after")
    def validar(self) -> ApontamentoCreate:
        validar_horarios(
            self.hora_entrada, self.saida_almoco, self.volta_almoco, self.hora_saida
        )
        return self


class ApontamentoUpdate(BaseModel):
    data: date | None = None
    hora_entrada: time | None = None
    saida_almoco: time | None = None
    volta_almoco: time | None = None
    hora_saida: time | None = None


class ApontamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    funcionario_id: uuid.UUID
    data: date
    hora_entrada: time
    saida_almoco: time | None = None
    volta_almoco: time | None = None
    hora_saida: time

    @computed_field
    @property
    def total_horas(self) -> Decimal:
        return calcular_total_horas(
            self.hora_entrada, self.saida_almoco, self.volta_almoco, self.hora_saida
        )
