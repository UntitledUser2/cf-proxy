import os
import httpx

BASE_URL = "https://api.curseforge.com/v1"

def headers():
    return {
        "x-api-key": os.getenv("CURSEFORGE_API_KEY"),
        "Accept": "application/json"
    }

async def search_mods(query: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BASE_URL}/mods/search",
            headers=headers(),
            params={"searchFilter": query, "gameId": 432}
        )
        r.raise_for_status()
        return r.json()