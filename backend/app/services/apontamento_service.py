from datetime import date
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.apontamento import Apontamento
from app.schemas.apontamento import ApontamentoCreate
from app.services import funcionario_service


def criar(session: Session, dados: ApontamentoCreate) -> Apontamento:
    funcionario = funcionario_service.obter(session, dados.funcionario_id)

    if not funcionario.ativo:
        raise HTTPException(
            status_code=422, detail="O funcionário informado está inativo."
        )

    consulta = select(Apontamento).where(
        and_(
            Apontamento.funcionario_id == dados.funcionario_id,
            Apontamento.data == dados.data,
        )
    )

    conflito_existente = session.scalars(consulta).first()

    if conflito_existente is not None:
        raise HTTPException(
            status_code=409,
            detail="Já existe um apontamento para este funcionário nesta data.",
        )

    apontamento = Apontamento(**dados.model_dump())
    session.add(apontamento)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Já existe um apontamento para este funcionário nesta data.",
        )

    session.refresh(apontamento)
    return apontamento


def listar(
    session: Session,
    funcionario_id: UUID | None = None,
    inicio: date | None = None,
    fim: date | None = None,
) -> list[Apontamento]:

    consulta = select(Apontamento).order_by(Apontamento.data)

    if funcionario_id is not None:
        consulta = consulta.where(Apontamento.funcionario_id == funcionario_id)

    if inicio is not None:
        consulta = consulta.where(Apontamento.data >= inicio)

    if fim is not None:
        consulta = consulta.where(Apontamento.data <= fim)

    return list(session.scalars(consulta).all())


def obter(session: Session, apontamento_id: UUID) -> Apontamento:
    apontamento = session.get(Apontamento, apontamento_id)
    if apontamento is None:
        raise HTTPException(status_code=404, detail="Apontamento não encontrado.")
    return apontamento
