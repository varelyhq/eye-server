from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class RatingIn(BaseModel):
    rating: int = Field(ge=0, le=5)

class RatingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rating: int
