import json
import aiosqlite
from app.database.db import DB_PATH

async def save_report(user_id: int, report: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "INSERT INTO reports (user_id, report) VALUES(?,?)",
                (user_id ,json.dumps(report))
            )
            await db.commit()
            return cursor.lastrowid
    
async def get_report(report_id: int) -> dict:
       async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "SELECT report FROM reports WHERE id=?",
                (report_id,)
            )
            row = await cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
                  