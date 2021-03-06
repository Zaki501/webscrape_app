from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import core.schemas as schemas
from api.security import get_current_active_user
from core.crud import delete_user
from core.database import get_db

router = APIRouter(tags=["User"], prefix="/api/user")


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: schemas.UserInDB = Depends(get_current_active_user),
):
    return current_user


@router.delete("/delete")
async def delete_user_me(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return delete_user(db, current_user.id)


@router.patch("/update")
async def update_user_me(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # while logged in
    # user re enters password, and fills out form
    # if password matches (check this in front end), update user details
    return {"message": "test"}
