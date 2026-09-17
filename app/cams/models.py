from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, TimestampMixin, SerializerMixin

class Cam(Base, TimestampMixin, SerializerMixin):
    __tablename__ = "cams"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(unique=True, index=True)

    name: Mapped[str]
    title: Mapped[str]
    image: Mapped[str]
    stream_url: Mapped[str | None]
    description: Mapped[str | None]
    original_url: Mapped[str]
    is_online: Mapped[bool] = mapped_column(default=True)

    views: Mapped[int] = mapped_column(default=0)
    rating_sum: Mapped[int] = mapped_column(default=0)
    rating_count: Mapped[int] = mapped_column(default=0)

class UserCamView(Base, TimestampMixin, SerializerMixin):
    __tablename__ = 'user_cam_view'

    __table_args__ = (
        UniqueConstraint("cam_id", "ip_address", name="uq_user_cam_view"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cam_id: Mapped[int] = mapped_column(ForeignKey('cams.id'))
    ip_address: Mapped[str] = mapped_column(index=True)
