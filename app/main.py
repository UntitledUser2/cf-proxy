from fastapi import FastAPI, Query
from app.curseforge import search_mods, get_mod, get_mod_files, find_game

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search")
async def search(
    q:         str = "",
    pageSize:  int = 20,
    index:     int = 0,
    sort:      str = "",
):
    return await search_mods(query=q, page_size=pageSize, index=index, sort=sort)

@app.get("/mod/{mod_id}")
async def mod(mod_id: int):
    return await get_mod(mod_id)

@app.get("/mod/{mod_id}/files")
async def mod_files(mod_id: int):
    return await get_mod_files(mod_id)

@app.get("/games/find")
async def games_find(slug: str = "subnautica-2"):
    """Utility endpoint — returns CurseForge game data for a given slug."""
    return await find_game(slug)
