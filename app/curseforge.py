import os
import httpx

BASE_URL = "https://api.curseforge.com/v1"
GAME_ID  = 99704   # Subnautica 2 — update if needed

# CurseForge ModsSearchSortField enum values (from API docs)
SORT_FIELDS = {
    "featured":    1,
    "popularity":  2,
    "updated":     3,
    "name":        4,
    "author":      5,
    "downloads":   6,
}

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
        sort_int = SORT_FIELDS.get(sort.lower())
        if sort_int:
            params["sortField"] = sort_int
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
    params = {"pageSize": 10, "index": 0}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/mods/{mod_id}/files", headers=headers(), params=params)
        r.raise_for_status()
        return r.json()

async def find_game(slug: str):
    """Utility: look up a game's numeric ID by slug."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/games", headers=headers())
        r.raise_for_status()
        data = r.json().get("data", [])
        matches = [g for g in data if g.get("slug") == slug]
        return matches[0] if matches else {"error": f"No game found with slug '{slug}'"}
