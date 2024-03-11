from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

router = APIRouter(
    prefix='/health',
    tags=['health']
)


class HealthCheck(BaseModel):
    status: str = "OK"

@router.get("/", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def get_health() -> HealthCheck:
    return HealthCheck(status="OK")