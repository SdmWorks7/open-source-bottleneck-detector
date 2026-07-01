import aiosqlite

DB_PATH = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                         
                         CREATE TABLE IF NOT EXISTS messages(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER NOT NULL,
                         message TEXT NOT NULL,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                         )
                         """)
        
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS memories(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER NOT NULL,
                         type TEXT NOT NULL,
                         value TEXT NOT NULL)""")


        await db.execute("""
                         CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         github_username TEXT)""")

        await db.execute("""
                         CREATE TABLE IF NOT EXISTS reports (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER NOT NULL,
                         report TEXT NOT NULL,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
        await db.commit()

