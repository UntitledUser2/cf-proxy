from fastapi import FastAPI
from app.curseforge import search_mods

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/search")
async def search(q: str):
    return await search_mods(q)