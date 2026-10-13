from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import HTTPException
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate

class ClienteDB(ClienteCreate):
    id: UUID
    ativo: bool
    created_at: datetime


_cliente: dict[UUID, ClienteDB] = {}

def criar(dados: ClienteCreate) -> ClienteDB:
    if dados.cnpj:

        cnpj_existente = any(cliente.cnpj == dados.cnpj for cliente in _cliente.values())

        if cnpj_existente:
            raise HTTPException(
                status_code=409,
                detail="Já existe um cliente cadastrado com este CNPJ!"
            )

    novo_cliente = ClienteDB(
        **dados.model_dump(),
        id=uuid4(),
        ativo=True,
        created_at=datetime.now(timezone.utc)
    )
    _cliente[novo_cliente.id] = novo_cliente
    return novo_cliente
        

def listar(ativo: bool | None = None) -> list[ClienteDB]:

    return [
        c for c in _cliente.values() 
        if (ativo is None) or (c.ativo == ativo)
    ]


def obter(cliente_id: UUID) -> ClienteDB:
    if cliente_id not in _cliente:
        raise HTTPException(
            status_code=404,
            detail="Nenhum cliente encontrado"
        )
    
    return _cliente[cliente_id]

def atualizar(cliente_id: UUID, dados: ClienteUpdate) -> ClienteDB:
    cliente = obter(cliente_id)
    valores_para_atualizar = dados.model_dump(exclude_unset=True)

    if "cnpj" in valores_para_atualizar and valores_para_atualizar["cnpj"] is not None:
        cnpj_existente = any(c.cnpj == dados.cnpj for id_cadastrado, c in _cliente.items() if id_cadastrado != cliente_id)

        if cnpj_existente:
            raise HTTPException(
                status_code=409,
                 detail="Este CNPJ já está cadastrado."
            )
    
    cliente_atualizado = cliente.model_copy(update=valores_para_atualizar)
    _cliente[cliente_id] = cliente_atualizado

    return cliente_atualizado
        
    

def deletar(cliente_id: UUID) -> None:
    cliente = obter(cliente_id)
    cliente_desativado = cliente.model_copy(update = {"ative": False})
    _cliente[cliente_id] = cliente_desativado