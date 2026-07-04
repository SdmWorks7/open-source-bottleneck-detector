from fastapi import APIRouter
from app.services.github_service import get_github_username, fetch_github_events, fetch_github_profile,process_github_stats

router = APIRouter()

@router.get("/github/{user_id}")
async def github(user_id):
    username =  await get_github_username(user_id)
    events= await fetch_github_events(username)
    profile=await fetch_github_profile(username)
    stats=  process_github_stats(events)
    return{"username": username,
           "profile": profile,
           "stats":stats}