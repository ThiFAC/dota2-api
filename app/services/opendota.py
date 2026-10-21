import httpx
from fastapi import HTTPException


BASE_URL = "https://api.opendota.com/api"


async def get_opendota_json(path: str):
    url = f"{BASE_URL}/{path.lstrip('/')}"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="A OpenDota demorou para responder.",
        ) from exc

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="A OpenDota respondeu com erro.",
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível conectar à OpenDota.",
        ) from exc