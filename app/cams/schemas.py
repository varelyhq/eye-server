from typing import Optional
from pydantic import BaseModel, ConfigDict

class CamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str

    name: str
    title: str
    image: str
    stream_url: Optional[str]
    is_online: bool

    views: int
    rating_sum: float
    rating_count: int

class FavoriteIdsIn(BaseModel):
    ids: list[int]
