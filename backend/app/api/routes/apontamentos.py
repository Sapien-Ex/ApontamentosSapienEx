from datetime import date
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.apontamento import (
    ApontamentoCreate,
    ApontamentoRead,
    ApontamentoUpdate,
)
from app.services import apontamento_service

router = APIRouter(prefix="/apontamentos", tags=["apontamentos"])


@router.post("/", response_model=ApontamentoRead, status_code=HTTPStatus.CREATED)
def criar_apontamento(session: SessionDep, dados: ApontamentoCreate):
    return apontamento_service.criar(session, dados)


@router.get("/", response_model=list[ApontamentoRead], status_code=HTTPStatus.OK)
def listar_apontamentos(
    session: SessionDep,
    funcionario_id: UUID | None = None,
    inicio: date | None = None,
    fim: date | None = None,
):
    return apontamento_service.listar(
        session, funcionario_id=funcionario_id, inicio=inicio, fim=fim
    )


@router.get(
    "/{apontamento_id}", response_model=ApontamentoRead, status_code=HTTPStatus.OK
)
def obter_apontamento(session: SessionDep, apontamento_id: UUID):
    return apontamento_service.obter(session, apontamento_id)


@router.patch(
    "/{apontamento_id}", response_model=ApontamentoRead, status_code=HTTPStatus.OK
)
def atualizar_apontamento(
    session: SessionDep, apontamento_id: UUID, dados: ApontamentoUpdate
):
    return apontamento_service.atualizar(session, apontamento_id, dados)


@router.delete("/{apontamento_id}", status_code=HTTPStatus.NO_CONTENT)
def excluir_apontamento(session: SessionDep, apontamento_id: UUID):
    apontamento_service.excluir(session, apontamento_id)
