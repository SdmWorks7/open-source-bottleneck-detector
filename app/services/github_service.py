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

async def fetch_github_profile(username: str) -> dict:
    url = f"https://api.github.com/users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
    
def process_github_stats(events: list) -> dict:
    push_count = 0
    pr_count = 0
    issue_count = 0

    for event in events:
        if event["type"] == "PushEvent":
            push_count += 1
        elif event["type"] == "PullRequestEvent":
            pr_count += 1
        elif event["type"] == "IssuesEvent":
            issue_count += 1

    return {
        "recent_pushes": push_count,
        "recent_prs": pr_count,
        "recent_issues": issue_count
    }