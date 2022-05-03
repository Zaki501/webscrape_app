from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import core.schemas as schemas
from api.security import get_current_active_user
from app.FirefoxWebDriver import FireFoxBrowser
from app.main import extract_asin, track_item
from core.crud import (
    check_alerts,
    create_alert,
    create_item,
    read_alerts,
    read_item_by_asin,
    toggle_item,
)
from core.database import get_db

router = APIRouter(tags=["Alert"], prefix="/api/alert")


@router.get("/all")
async def all_alerts(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return read_alerts(db, current_user.id)


@router.get("/new")
async def create_new_alert(
    amazon_url: str,
    target_price: Decimal,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """While logged in, user sends amazon url of item to be tracked.
    Check if item is already being tracked, then add alert for user."""

    # extract asin, look for item in db
    asin = extract_asin(amazon_url)
    item = read_item_by_asin(db, asin)

    # check if user already has alert for this item
    if check_alerts(db, current_user.id, asin) is not None:
        raise HTTPException(
            status_code=400, detail="User already has alert for this item"
        )

    # check number of alerts
    alerts = read_alerts(db, current_user.id)
    if len(alerts) >= 5:
        raise HTTPException(status_code=400, detail="User has reached max alerts")

    # if item is deactivated, enable it
    if item is not None and item.disabled is True:
        toggle_item(db, item.id)

    # if item doesnt exist, create it
    if item is None:
        # scrape pricehistory
        browser = FireFoxBrowser(headless=False, random_user_agent=False)
        with browser:
            p_h = track_item(browser, asin)
        create_item(db, p_h)
    return create_alert(db, current_user.id, target_price, p_h)
