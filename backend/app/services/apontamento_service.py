from datetime import date
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.apontamento import Apontamento
from app.schemas.apontamento import ApontamentoCreate, ApontamentoUpdate
from app.services import funcionario_service
from app.services.calculo_horas import validar_horarios


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


def atualizar(
    session: Session, apontamento_id: UUID, dados: ApontamentoUpdate
) -> Apontamento:
    apontamento = obter(session, apontamento_id)
    dados_novos = dados.model_dump(exclude_unset=True)

    hora_entrada = dados_novos.get("hora_entrada", apontamento.hora_entrada)
    saida_almoco = dados_novos.get("saida_almoco", apontamento.saida_almoco)
    volta_almoco = dados_novos.get("volta_almoco", apontamento.volta_almoco)
    hora_saida = dados_novos.get("hora_saida", apontamento.hora_saida)

    try:
        validar_horarios(hora_entrada, saida_almoco, volta_almoco, hora_saida)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))

    nova_data = dados_novos.get("data", apontamento.data)
    if nova_data != apontamento.data:
        consulta = select(Apontamento).where(
            and_(
                Apontamento.funcionario_id == apontamento.funcionario_id,
                Apontamento.data == nova_data,
            )
        )

        if session.scalars(consulta).first() is not None:
            raise HTTPException(
                status_code=409,
                detail="Já existe um apontamento para este funcionário nesta data.",
            )

    for campo, valor in dados_novos.items():
        setattr(apontamento, campo, valor)

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
