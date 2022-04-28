from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import core.crud as crud
import core.schemas as schemas
from api.security import authenticate_user, create_access_token
from core.database import get_db
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, generate_token
from limiter import limiter

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
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    db_user = crud.read_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/forgot_password")
async def send_token_to_email(
    email: str, request: Request, db: Session = Depends(get_db)
):
    # create token, store in ResetPassword
    # send token to users email, as URL

    # user enters email for forgotten password
    # if user doesnt exist, raise error
    # create token for user, send in email
    # hash token and add to db

    # current tokens are security risk? they are the same each minute
    # rate? limit users password guesses
    # check if reset request already sent

    # totp tokens are time-based, and independent of client and server
    # look into google auth

    # if user not in users table, return error
    # if user in resetpassword table, delete them

    user = crud.read_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=400, detail="Email doesn't exist")
    if crud.read_password_reset(db, email) is not None:
        crud.delete_password_reset(db, email)
    token = generate_token()
    crud.create_password_reset(db, email, token)
    return {
        "message": "Reset Code sent to email",
        "token": token,
        "url": f"{request.base_url}",
        "url2": f"{request.base_url}api/auth/reset_password/{email}&{token}",
    }


@router.get("/reset_password/{email}&{token}")
@limiter.limit("3/minute")
async def new_password(
    email: str, token: str, request: Request, db: Session = Depends(get_db)
):
    """Rate limited - 3 attempts per minute"""
    # match email and token to db

    # if no match, raise error "link already used, request another"
    # if is expire, raise error "link expired, request another"
    # email and token matches - allow user to choose new password

    return {"email": email, "token": token, "url": request.url._url}
