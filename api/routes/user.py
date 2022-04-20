from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import core.schemas as schemas
from api.security import get_current_active_user
from core.crud import check_alerts
from core.database import get_db

router = APIRouter(tags=["User"], prefix="/api/user")


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/all")
async def read_users_all(
    asin: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return check_alerts(db, current_user.id, asin)


# change password
# change email
# change name
