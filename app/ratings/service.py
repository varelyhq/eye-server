from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from .models import Rating
from ..cams.models import Cam
from ..database import async_session

async def get_user_rating(cam_id: int, user_id: str) -> Rating:
    async with async_session() as session:
        statement = select(Rating).where(Rating.cam_id == cam_id, Rating.user_id == user_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

async def set_user_cam_rating(cam_id: int, user_id: str, rating: int) -> Rating:
    data = { "cam_id": cam_id, "user_id": user_id, "rating": rating }

    async with async_session() as session:
        async with session.begin():
            cam = await session.scalar(
                select(Cam).where(Cam.id == cam_id).with_for_update()
            )

            existing = await session.scalar(
                select(Rating).where(
                    Rating.cam_id == cam_id,
                    Rating.user_id == user_id,
                )
            )

            stmt = insert(Rating).values(**data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["cam_id", "user_id"],
                set_={ "rating": stmt.excluded.rating },
            ).returning(Rating)
            new_rating = (await session.execute(stmt)).scalar_one()

            old_rating = existing.rating if existing is not None else 0
            sum_delta = rating - old_rating

            old_active = old_rating > 0
            new_active = rating > 0

            if old_active and new_active: count_delta = 0
            elif old_active and not new_active: count_delta = -1
            elif not old_active and new_active: count_delta = 1
            else: count_delta = 0

            await session.execute(
                update(Cam).where(Cam.id == cam_id)
                .values(
                    rating_sum=Cam.rating_sum + sum_delta,
                    rating_count=Cam.rating_count + count_delta
                )
            )

        await session.refresh(new_rating)
        return new_rating
