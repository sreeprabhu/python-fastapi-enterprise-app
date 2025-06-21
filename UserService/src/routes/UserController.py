from fastapi import APIRouter, Depends

from UserService.src.dependencies import get_user_service
from UserService.src.repository.services import UserService

router = APIRouter(
    prefix="/users"
)

@router.get("", status_code=200)
async def get_user(
    email: str,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user(email=email)


# Now, finally we are at our Controller layer, and as you can see we are using Dependency Injection, which is extremely popular in FastAPI. 
# You see our endpoints depend on get_user_service and assigns whatever this function returns (Spoiler, it’s a UserService instance) to the user_servicevariable.