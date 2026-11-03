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
            status_code=422, detail="O funcionário informado está inativo"
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
        raise HTTPException(status_code=409, detail="Já existe um apontamento")

    session.refresh(apontamento)
    return apontamento
