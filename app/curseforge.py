import os
import httpx

BASE_URL = "https://api.curseforge.com/v1"
GAME_ID  = 99704   # Subnautica 2 — confirmed via /games/find endpoint

def headers():
    return {
        "x-api-key": os.getenv("CURSEFORGE_API_KEY"),
        "Accept":    "application/json",
    }

async def search_mods(query: str = "", page_size: int = 20, index: int = 0, sort: str = ""):
    params = {
        "gameId":       GAME_ID,
        "searchFilter": query,
        "pageSize":     page_size,
        "index":        index,
    }
    if sort:
        params["sortField"] = sort
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/mods/search", headers=headers(), params=params)
        r.raise_for_status()
        return r.json()

async def get_mod(mod_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/mods/{mod_id}", headers=headers())
        r.raise_for_status()
        return r.json()

async def get_mod_files(mod_id: int):
    params = {"pageSize": 10, "sortOrder": "desc"}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/mods/{mod_id}/files", headers=headers(), params=params)
        r.raise_for_status()
        return r.json()

async def find_game(slug: str):
    """Helper to look up a game's numeric ID by its slug. Used to verify GAME_ID."""
    params = {"slug": slug}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/games", headers=headers(), params=params)
        r.raise_for_status()
        return r.json()
