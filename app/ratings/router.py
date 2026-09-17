from fastapi import APIRouter, Response, status

from . import service
from .schemas import RatingIn, RatingOut

from ..auth.dependencies import CurrentUserId
from ..common.schemas import SuccessResponse

router = APIRouter()

@router.get("/{cam_id}", response_model=SuccessResponse[RatingOut | None])
async def get_user_rating(cam_id: int, user_id: CurrentUserId):
    rating = await service.get_user_rating(cam_id, user_id)
    return SuccessResponse(rating)

@router.post("/{cam_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_cam_rating(cam_id: int, body: RatingIn, user_id: CurrentUserId) -> None:
    await service.set_user_cam_rating(cam_id=cam_id, user_id=user_id, rating=body.rating)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
