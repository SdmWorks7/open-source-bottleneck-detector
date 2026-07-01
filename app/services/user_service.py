import aiosqlite
from app.database.db import DB_PATH

async def save_github_username(user_id: int, github_username: str):
     async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO users (id,github_username) VALUES(?,?)",
            (user_id,github_username)
        )
        await db.commit()
        return cursor.lastrowid