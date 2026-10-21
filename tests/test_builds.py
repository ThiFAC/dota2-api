import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_crud_completo_de_build(client):
    headers = {"X-API-Key": settings.api_key}

    dados = {
        "name": "Build de teste",
        "hero_id": 2,
        "items": ["Blink Dagger"],
        "skill_order": ["Berserkers Call"],
        "description": "Build criada pelo teste.",
    }

    resposta_criar = client.post(
        "/api/v1/builds",
        json=dados,
        headers=headers,
    )

    assert resposta_criar.status_code == 201
    build_id = resposta_criar.json()["id"]

    resposta_listar = client.get("/api/v1/builds")

    assert resposta_listar.status_code == 200
    assert len(resposta_listar.json()) == 1

    resposta_atualizar = client.patch(
        f"/api/v1/builds/{build_id}",
        json={"description": "Build atualizada."},
        headers=headers,
    )

    assert resposta_atualizar.status_code == 200
    assert resposta_atualizar.json()["description"] == "Build atualizada."

    resposta_excluir = client.delete(
        f"/api/v1/builds/{build_id}",
        headers=headers,
    )

    assert resposta_excluir.status_code == 204

    resposta_depois_de_excluir = client.get(
        f"/api/v1/builds/{build_id}"
    )

    assert resposta_depois_de_excluir.status_code == 404