from sqlalchemy import CheckConstraint, UniqueConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base

class Rating(Base):
    __tablename__ = "ratings"

    __table_args__ = (
        UniqueConstraint("cam_id", "user_id", name="uq_rating_cam_user"),
        CheckConstraint("rating >= 0 AND rating <= 5"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cam_id: Mapped[int] = mapped_column(ForeignKey("cams.id"))
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    rating: Mapped[int]
