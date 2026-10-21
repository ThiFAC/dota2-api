from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import Build
from app.routes import builds, heroes


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API própria para consultar heróis e manter builds de Dota 2.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "X-API-Key"],
)


app.include_router(heroes.router, prefix="/api/v1")
app.include_router(builds.router, prefix="/api/v1")


@app.get("/health", tags=["Saúde"])
def verificar_saude():
    return {"status": "ok"}