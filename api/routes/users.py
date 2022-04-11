from fastapi import APIRouter, Depends

from api.security import get_current_active_user
from core.schemas import User

router = APIRouter(tags=["User"], prefix="/api/user")


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
