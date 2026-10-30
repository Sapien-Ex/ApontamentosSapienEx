from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.funcionario import (
    FuncionarioCreate,
    FuncionarioRead,
    FuncionarioUpdate,
)
from app.services import funcionario_service

router = APIRouter(prefix="/funcionarios", tags=["funcionários"])


@router.post("/", response_model=FuncionarioRead, status_code=HTTPStatus.CREATED)
def criar_funcionario(session: SessionDep, dados: FuncionarioCreate):
    return funcionario_service.criar(session, dados)


@router.get("/", response_model=list[FuncionarioRead], status_code=HTTPStatus.OK)
def listar_funcionarios(session: SessionDep, ativo: bool | None = None):
    return funcionario_service.listar(session, ativo)


@router.get(
    "/{funcionario_id}", response_model=FuncionarioRead, status_code=HTTPStatus.OK
)
def obter_funcionario(session: SessionDep, funcionario_id: UUID):
    return funcionario_service.obter(session, funcionario_id)


@router.patch(
    "/{funcionario_id}", response_model=FuncionarioRead, status_code=HTTPStatus.OK
)
def atualizar_funcionario(
    session: SessionDep, funcionario_id: UUID, dados: FuncionarioUpdate
):
    return funcionario_service.atualizar(session, funcionario_id, dados)


@router.delete(
    "/{funcionario_id}", response_model=FuncionarioRead, status_code=HTTPStatus.OK
)
def desativar_funcionario(session: SessionDep, funcionario_id: UUID):
    return funcionario_service.desativar(session, funcionario_id)
