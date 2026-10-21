from pydantic import BaseModel, ConfigDict, Field


class BuildCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    hero_id: int = Field(gt=0)
    items: list[str] = Field(default_factory=list)
    skill_order: list[str] = Field(default_factory=list)
    passive_abilities: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=1000)


class BuildUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    hero_id: int | None = Field(default=None, gt=0)
    items: list[str] | None = None
    skill_order: list[str] | None = None
    passive_abilities: list[str] | None = None
    description: str | None = Field(default=None, max_length=1000)


class BuildRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    hero_id: int
    items: list[str]
    skill_order: list[str]
    passive_abilities: list[str]
    description: str | None