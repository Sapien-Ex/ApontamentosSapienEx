from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.funcionario import Funcionario
from app.schemas.funcionario import FuncionarioCreate, FuncionarioUpdate


def criar(session: Session, dados: FuncionarioCreate) -> Funcionario:
    funcionario = Funcionario(**dados.model_dump())
    session.add(funcionario)
    session.commit()
    session.refresh(funcionario)
    return funcionario


def listar(session: Session, ativo: bool | None = None) -> list[Funcionario]:
    consulta = select(Funcionario).order_by(Funcionario.nome)
    if ativo is not None:
        consulta = consulta.where(Funcionario.ativo == True)
    return list(session.scalars(consulta).all())


def obter(session: Session, funcionario_id: UUID) -> Funcionario:
    funcionario = session.get(Funcionario, funcionario_id)
    if funcionario is None:
        raise HTTPException(status_code=404, details="Funcionário não encontrado!")
    return funcionario


def atualizar(
    session: Session, funcionario_id: UUID, dados: FuncionarioUpdate
) -> Funcionario:
    funcionario = obter(session, funcionario_id)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(funcionario, campo, valor)
        session.commit()
        session.refresh(funcionario)
    return funcionario


def desativar(session: Session, funcionario_id: UUID) -> Funcionario:
    funcionario = obter(session, funcionario_id)
    funcionario.ativo = False
    session.commit()
    session.refresh(funcionario)
    return funcionario
