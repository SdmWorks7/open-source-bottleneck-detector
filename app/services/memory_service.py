# IMP: extract_memories() and get_memories() are deprecated as of the latest version
# Memory extraction and retrieval is now handled by cognee_service.py using Cognee Cloud.
# save_memories() is kept for potential fallback/backup purposes.
# These functions may be removed in a future cleanup.


import aiosqlite
from app.database.db import DB_PATH


SKILL_KEYWORDS = ["java", "python", "javascript", "react", "sql", "fastapi"]
WEAKNESS_KEYWORDS = ["git", "github", "debugging", "testing", "deployment"]

def extract_memories(message: str)->list:
    message_lower = message.lower()
    memories = []

    for skill in SKILL_KEYWORDS:
        if skill in message_lower:
            memories.append({"type":"skill", "value":skill})

    for weakness in WEAKNESS_KEYWORDS:
        if weakness in message_lower:
            memories.append({"type": "weakness", "value": weakness}) 

    return memories

async def save_memories(user_id: int, memories: list) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        for memory in memories:
            cursor = await db.execute(
                "INSERT INTO memories (user_id, type, value) VALUES(?,?,?)",
                (user_id ,memory["type"], memory["value"])
            )
            await db.commit()

async def get_memories(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT type, value FROM memories WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchall()
        return [{"type": r[0], "value": r[1]} for r in row]
