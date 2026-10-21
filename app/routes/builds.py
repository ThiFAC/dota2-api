from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Build
from app.schemas import BuildCreate, BuildRead, BuildUpdate
from app.security import require_api_key


router = APIRouter(
    prefix="/builds",
    tags=["Builds"],
)


DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[BuildRead])
def listar_builds(
    db: DbSession,
    hero_id: int | None = Query(default=None, gt=0),
    q: str | None = Query(default=None, min_length=1, max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    statement = select(Build)

    if hero_id is not None:
        statement = statement.where(Build.hero_id == hero_id)

    if q:
        statement = statement.where(Build.name.ilike(f"%{q}%"))

    statement = statement.order_by(Build.id).offset(offset).limit(limit)

    return db.scalars(statement).all()


@router.get("/{build_id}", response_model=BuildRead)
def consultar_build(
    build_id: int,
    db: DbSession,
):
    build = db.get(Build, build_id)

    if build is None:
        raise HTTPException(
            status_code=404,
            detail="Build não encontrada.",
        )

    return build


@router.post(
    "",
    response_model=BuildRead,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
def criar_build(
    payload: BuildCreate,
    db: DbSession,
):
    build = Build(**payload.model_dump())

    db.add(build)
    db.commit()
    db.refresh(build)

    return build


@router.patch(
    "/{build_id}",
    response_model=BuildRead,
    dependencies=[Depends(require_api_key)],
)
def atualizar_build(
    build_id: int,
    payload: BuildUpdate,
    db: DbSession,
):
    build = db.get(Build, build_id)

    if build is None:
        raise HTTPException(
            status_code=404,
            detail="Build não encontrada.",
        )

    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Envie pelo menos um campo para atualizar.",
        )

    fields_that_cannot_be_null = (
        "name",
        "hero_id",
        "items",
        "skill_order",
        "passive_abilities",
    )

    for field in fields_that_cannot_be_null:
        if field in changes and changes[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"O campo '{field}' não pode ser nulo.",
            )

    for field, value in changes.items():
        setattr(build, field, value)

    db.commit()
    db.refresh(build)

    return build


@router.delete(
    "/{build_id}",
    status_code=204,
    dependencies=[Depends(require_api_key)],
)
def excluir_build(
    build_id: int,
    db: DbSession,
):
    build = db.get(Build, build_id)

    if build is None:
        raise HTTPException(
            status_code=404,
            detail="Build não encontrada.",
        )

    db.delete(build)
    db.commit()

    return Response(status_code=204)