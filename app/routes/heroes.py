from fastapi import APIRouter, HTTPException, Query

from app.services.opendota import get_opendota_json


router = APIRouter(
    prefix="/heroes",
    tags=["Heróis"],
)

CDN_BASE = "https://cdn.cloudflare.steamstatic.com"


def image_url_from_path(path: str | None) -> str | None:
    if not path:
        return None

    if path.startswith("http://") or path.startswith("https://"):
        return path

    if path.startswith("/"):
        return f"{CDN_BASE}{path}"

    return f"{CDN_BASE}/{path}"


def ability_image_url(
    ability_name: str,
    ability_data: dict,
) -> str:
    image = image_url_from_path(ability_data.get("img"))

    if image:
        return image

    return (
        f"{CDN_BASE}/apps/dota2/images/"
        f"dota_react/abilities/{ability_name}.png"
    )


@router.get("/items")
async def listar_itens():
    data = await get_opendota_json("constants/items")
    result = []

    for item_id, item in data.items():
        if not isinstance(item, dict):
            continue

        if not item.get("dname") or not item.get("img"):
            continue

        result.append({
            "id": str(item_id),
            "name": item["dname"],
            "image_url": image_url_from_path(item.get("img")),
            "cost": item.get("cost"),
        })

    result.sort(key=lambda item: item["name"].casefold())
    return result


@router.get("")
async def listar_herois(
    q: str | None = Query(default=None, min_length=1, max_length=50),
):
    heroes = await get_opendota_json("heroStats")

    if q:
        term = q.casefold()
        heroes = [
            hero
            for hero in heroes
            if term in hero.get("localized_name", "").casefold()
        ]

    result = []

    for hero in heroes:
        hero_data = hero.copy()
        hero_data["image_url"] = image_url_from_path(hero.get("img"))
        result.append(hero_data)

    return result


@router.get("/{hero_id}/abilities")
async def consultar_habilidades(hero_id: int):
    heroes = await get_opendota_json("heroStats")

    hero = next(
        (item for item in heroes if item.get("id") == hero_id),
        None,
    )

    if hero is None:
        raise HTTPException(
            status_code=404,
            detail="Herói não encontrado.",
        )

    abilities_by_hero = await get_opendota_json(
        "constants/hero_abilities"
    )
    all_abilities = await get_opendota_json(
        "constants/abilities"
    )

    hero_key = hero.get("name")
    hero_data = abilities_by_hero.get(hero_key)

    if not hero_data:
        raise HTTPException(
            status_code=502,
            detail="A OpenDota não retornou as habilidades desse herói.",
        )

    result = []

    for ability_name in hero_data.get("abilities", []):
        ability_data = all_abilities.get(ability_name, {})

        behavior = ability_data.get("behavior", "")

        if isinstance(behavior, list):
            behavior = " ".join(str(value) for value in behavior)

        is_passive = "PASSIVE" in str(behavior).upper()

        result.append({
            "name": ability_name,
            "display_name": ability_data.get("dname") or ability_name,
            "description": ability_data.get("desc") or "",
            "image_url": ability_image_url(
                ability_name,
                ability_data,
            ),
            "is_passive": is_passive,
        })

    return {
        "hero_id": hero["id"],
        "hero_name": hero.get("localized_name"),
        "abilities": result,
    }


@router.get("/{hero_id}")
async def consultar_heroi(hero_id: int):
    heroes = await get_opendota_json("heroStats")

    hero = next(
        (item for item in heroes if item.get("id") == hero_id),
        None,
    )

    if hero is None:
        raise HTTPException(
            status_code=404,
            detail="Herói não encontrado.",
        )

    hero_data = hero.copy()
    hero_data["image_url"] = image_url_from_path(hero.get("img"))
    return hero_data