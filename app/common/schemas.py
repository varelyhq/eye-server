from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T

    def __init__(self, data: T, **kwargs):
        super().__init__(data=data, **kwargs)

class FailedResponse(BaseModel):
    success: bool = False
    error_message: str

    def __init__(self, error_message: str, **kwargs):
        super().__init__(error_message=error_message, **kwargs)
