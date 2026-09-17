from typing import Optional
from sqlalchemy import select, update, func
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone, timedelta

from .models import Cam, UserCamView
from ..database import async_session

async def get_cam(cam_id: int) -> Optional[Cam]:
    async with async_session() as session:
        stmt = select(Cam).where(Cam.id == cam_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def get_cam_by_slug(slug: str) -> Optional[Cam]:
    async with async_session() as session:
        stmt = select(Cam).where(Cam.slug == slug)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def get_popular_cams() -> list[Cam]:
    async with async_session() as session:
        stmt = select(Cam).order_by(Cam.views.desc()).limit(10)
        results = await session.execute(stmt)
        return list(results.scalars().all())

async def get_cams_by_ids(ids: list[str]) -> list[Cam]:
    if not ids:
        return []
    async with async_session() as session:
        stmt = select(Cam).where(Cam.id.in_(ids))
        result = await session.execute(stmt)
        cams = list(result.scalars().all())
    order = { id_: idx for idx, id_ in enumerate(ids) }
    cams.sort(key=lambda c: order.get(c.id, len(order)))
    return cams

async def increment_cam_view(cam_id: int, ip_address: str):
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    async with async_session() as session:
        stmt = insert(UserCamView).values(cam_id=cam_id, ip_address=ip_address)
        stmt = stmt.on_conflict_do_update(
            index_elements=['cam_id', 'ip_address'],
            where=UserCamView.updated_at < one_hour_ago,
            set_={ "updated_at": func.now() },
        ).returning(UserCamView.cam_id)

        result = await session.execute(stmt)
        row = result.fetchone()

        if row is None:
            return False

        await session.execute(update(Cam).where(Cam.id == cam_id).values(views=Cam.views + 1))
        await session.commit()
        return True
