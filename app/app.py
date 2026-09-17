import socketio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv
load_dotenv()

from .sockets import sio
from .database import init_db
from .scraper import jobs as scraper_jobs
from .common.db_lifespan import dump_db_state

from .cams import router as cams_router
from .ratings import router as ratings_router

scheduler = AsyncIOScheduler()

from datetime import datetime
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await dump_db_state()
    scheduler.add_job(scraper_jobs.job_check_cams_status, 'interval', minutes=15, id='cams_15min', replace_existing=True)
    scheduler.add_job(scraper_jobs.job_full_scrape, 'cron', hour=3, minute=0, id='cams_daily', replace_existing=True, next_run_time=datetime.now())
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://eye.varely.co", "https://eye-b1un0d3js-varely.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

socket_app = CORSMiddleware(
    socket_app,
    allow_origins=[
        "http://localhost:3000",
        "https://eye.varely.co",
        "https://eye-b1un0d3js-varely.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cams_router, prefix='/cams', tags=['cams'])
app.include_router(ratings_router, prefix='/ratings', tags=['ratings'])

@app.get("/health")
async def health():
    return { "status": "ok" }
