from decimal import Decimal

from sqlalchemy.orm import Session

import core.models as models
import core.schemas as schemas
from api.security import create_hash


## Users
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = create_hash(user.password)

    db_user = models.User(
        email=user.email,
        disabled=False,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def read_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def read_all_users(db: Session):
    return db.query(models.User).all()


def update_user_email(db: Session, user: schemas.User, user_id: int):
    """ "asdad"""
    user_in_db = db.query(models.User).filter(models.User.id == user_id).first()
    user_in_db.email = user.email
    # return


def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"Message": "User succesfully deleted"}


## Items
# create pricehistory and update item every day
def create_item(db: Session, PriceHistory: schemas.Price_History):
    """Add item to database"""
    db_item = models.Item(
        asin=PriceHistory.asin,
        title=PriceHistory.title,
        currency=PriceHistory.currency,
        current_amount=PriceHistory.amount,
        disabled=False,
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def read_item_by_asin(db: Session, asin: int):
    return db.query(models.Item).filter(models.Item.asin == asin).first()


def update_item(db: Session, PriceHistory: schemas.Price_History):
    pass


def toggle_item(db: Session, item_id: int):
    """Flip bool, disable/enable item"""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    item.disabled = not item.disabled
    db.commit()
    db.refresh(item)
    return item


def delete_item():
    pass


## Alerts
# update and delete - target by id or asin?


def create_alert(
    db: Session, id: int, target_price: Decimal, PriceHistory: schemas.Price_History
):
    """Create alert for current user"""

    db_alert = models.Alert(
        asin=PriceHistory.asin, user_id=id, target_amount=target_price
    )

    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def read_alerts(db: Session, id: int):
    """Get all alerts for a user"""
    return db.query(models.Alert).filter(models.Alert.user_id == id).all()


def check_alerts(db: Session, id: int, asin: str):
    """see if a user a particalar item tracked"""
    return (
        db.query(models.Alert)
        .filter(models.Alert.user_id == id)
        .filter(models.Alert.asin == asin)
        .first()
    )


def update_alert(db: Session, alert_id: int, target_price: Decimal):
    """Update an existing alert with new target"""
    pass


def delete_alert(db: Session, alert_id: int):
    """Delete alert"""
    pass
