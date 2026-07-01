from fastapi import FastAPI
from app.api import chat, analyze, report, register
from app.database.db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router)
app.include_router(analyze.router)
app.include_router(report.router)
app.include_router(register.router)

@app.get("/")
def root():
    return {"status":"running"}
