from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, TimestampMixin, SerializerMixin

class Message(Base, TimestampMixin, SerializerMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    cam_id: Mapped[int] = mapped_column(ForeignKey('cams.id'))
    user_id: Mapped[str] = mapped_column(String(36))
    content: Mapped[str] = mapped_column(String(300))
    # username: Mapped[str | None] = mapped_column(String(32), nullable=True)
