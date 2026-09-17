import os
import asyncio
from sqlalchemy.dialects.postgresql import insert

from dotenv import load_dotenv
load_dotenv()

from ..cams.models import Cam
from ..database import async_session
from .scraper import scrape_sea_cams, scrape_single_cam

SEA_CAMS_URL = os.getenv('SEA_CAMS_URL')

async def upsert_cams(cams_data: list[dict]):
    async with async_session() as session:
        for data in cams_data:
            stmt = insert(Cam).values(**data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['slug'],
                set_={k: v for k, v in data.items() if k != 'slug'},
            )
            await session.execute(stmt)
        await session.commit()

async def job_check_cams_status():
    try:
        cams = await asyncio.to_thread(scrape_sea_cams, SEA_CAMS_URL)
        await upsert_cams(cams)
        print('JOB SUCCESS: check cams status:', 'successfully ended.')
    except Exception as e:
        print('JOB ERROR, check cams status:', e)

async def job_full_scrape():
    try:
        cams = await asyncio.to_thread(scrape_sea_cams, SEA_CAMS_URL)
        for cam in cams:
            details = await asyncio.to_thread(scrape_single_cam, cam['original_url'])
            cam.update(details)
        await upsert_cams(cams)
    except Exception as e:
        print('JOB ERROR, full scrape:', e)
