from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import core.schemas as schemas
from api.security import get_current_active_user
from app.FirefoxWebDriver import FireFoxBrowser
from app.main import extract_asin, track_item
from core.crud import create_alert, create_item, read_item_by_asin
from core.database import get_db

router = APIRouter(tags=["User"], prefix="/api/user")


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/new_item", response_model=schemas.Alert)
async def add_item_alert(
    amazon_url: str,
    target_price: Decimal,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """While logged in, user sends amazon url of item to be tracked.
    Check if item is already being tracked, then add alert for user."""
    # check number of alerts

    asin = extract_asin(amazon_url)
    browser = FireFoxBrowser(headless=False, random_user_agent=False)
    with browser:
        p_h = track_item(browser, asin)
    # check if item is inactive, if so activate
    if read_item_by_asin(db, asin) is None:
        create_item(db, p_h)
    return create_alert(db, current_user.id, target_price, p_h)
