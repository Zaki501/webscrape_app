from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import core.crud as crud
import core.schemas as schemas
from api.security import authenticate_user, create_access_token
from core.database import get_db
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Auth"], prefix="/api/auth")


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # try:
    return crud.create_user(db=db, user=user)
    # except IntegrityError:
    #     db.rollback()
    #     raise HTTPException(status_code=400, detail="Username already in use")


@router.post("/reset_password", response_model=schemas.User)
async def forgot_password(email: str, db: Session = Depends(get_db)):
    # user enters email for forgotten password
    # if user doesnt exist, raise error
    # create token for user, send in email
    # hash token and add to db

    # current tokens are security risk? they are the same each minute
    # rate? limit users password guesses
    # check if reset request already sent
    # disable user account while active

    # totp tokens are time-based, and independent of client and server
    # look into google auth
    pass
