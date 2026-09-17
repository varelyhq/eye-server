from typing import Annotated, Literal
from fastapi import APIRouter, HTTPException, Response, Request, Query

from . import service
from .schemas import CamOut, FavoriteIdsIn

from ..common.utils import get_client_ip
from ..common.schemas import SuccessResponse

router = APIRouter()

@router.get('/search', response_model=SuccessResponse[list[CamOut] | None])
async def search_cams(
        q: Annotated[str | None, Query(min_length=0, max_length=100)] = '',
        order_by: Annotated[Literal['default', 'popular', 'a-z', 'z-a'] | None, Query()] = None,
        show_inactive: Annotated[bool | None, Query()] = None,
        limit: Annotated[int | None, Query()] = 10,
    ):
    cams = await service.search_cams(q, order_by, show_inactive, limit)
    return SuccessResponse(cams)

@router.get('/popular', response_model=SuccessResponse[list[CamOut] | None])
async def get_popular_cams():
    cams = await service.get_popular_cams()
    return SuccessResponse(cams)

@router.post("/favorites", response_model=SuccessResponse[list[CamOut]])
async def get_favorite_cams(payload: FavoriteIdsIn):
    cams = await service.get_cams_by_ids(payload.ids)
    return SuccessResponse(cams)

@router.get("/cam/{cam_id}", response_model=SuccessResponse[CamOut])
async def get_cam(cam_id: int):
    cam = await service.get_cam(cam_id)
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found.")
    return SuccessResponse(cam)

@router.get("/slug/{slug}", response_model=SuccessResponse[CamOut])
async def get_cam_by_slug(slug: str):
    cam = await service.get_cam_by_slug(slug)
    if not cam:
        raise HTTPException(status_code=404, detail="Camera not found.")
    return SuccessResponse(cam)

@router.post("/cam/{cam_id}/view")
async def user_cam_view(cam_id: int, request: Request):
    ip_address = get_client_ip(request)
    await service.increment_cam_view(cam_id, ip_address)
    return Response(status_code=204)
