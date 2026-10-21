from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def agora_utc() -> datetime:
    return datetime.now(timezone.utc)


class Build(Base):
    __tablename__ = "builds"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    hero_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    # Os valores desta lista são os identificadores dos itens.
    items: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # Guarda os nomes internos das habilidades escolhidas.
    skill_order: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # Guarda separadamente as habilidades passivas escolhidas.
    passive_abilities: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=agora_utc,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=agora_utc,
        onupdate=agora_utc,
        nullable=False,
    )