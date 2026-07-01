import aiosqlite
from app.database.db import DB_PATH

async def save_message(user_id: int, message: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO messages (user_id, message) VALUES(?,?)",
            (user_id,message)
        )
        await db.commit()
        return cursor.lastrowid