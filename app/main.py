from fastapi import FastAPI
from app.api import chat, analyze, report, register, github
from app.database.db import init_db
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(analyze.router)
app.include_router(report.router)
app.include_router(register.router)
app.include_router(github.router)

@app.get("/")
def root():
    return {"status":"running"}

@app.get("/app")
def serve_frontend():
    return FileResponse("index.html")
