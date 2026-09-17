from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from .models import Message
from ..database import async_session

async def send_message(cam_id: int, user_id: str, content: str):
    async with async_session() as session:
        msg = Message(cam_id=cam_id, user_id=user_id, content=content)
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg.to_dict()

async def get_messages(cam_id: str):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    async with async_session() as session:
        stmt = (
            select(Message)
            .where(Message.cam_id == cam_id)
            .where(Message.created_at >= cutoff)
            .order_by(Message.created_at.asc())
            .limit(50)
        )
        messages = (await session.execute(stmt)).scalars().all()
        msgs = [m.to_dict() for m in messages]
        return msgs
