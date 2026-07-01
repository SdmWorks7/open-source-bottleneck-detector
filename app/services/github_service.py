import aiosqlite
import httpx
from app.database.db import DB_PATH


async def get_github_username(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT github_username FROM users WHERE id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None

async def fetch_github_events(username: str):
    url = f"https://api.github.com/users/{username}/events"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()