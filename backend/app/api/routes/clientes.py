from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from app.services import cliente_service

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteRead, status_code=HTTPStatus.CREATED)
def criar_cliente(dados: ClienteCreate):
    return cliente_service.criar(dados)


@router.get("/", response_model=list[ClienteRead])
def listar_clientes(ativo: bool | None = None):
    dados = cliente_service.listar(ativo)
    return dados


@router.get("/{cliente_id}", response_model=ClienteRead)
def obter_cliente(cliente_id: UUID):
    dado_cliente = cliente_service.obter(cliente_id)
    return dado_cliente


@router.patch("/{cliente_id}", response_model=ClienteRead)
def atualizar_cliente(cliente_id: UUID, dados: ClienteUpdate):
    return cliente_service.atualizar(cliente_id, dados)


@router.delete("/{cliente_id}", response_model=ClienteRead, status_code=HTTPStatus.OK)
def desativar_cliente(cliente_id: UUID):
    return cliente_service.desativar(cliente_id)
