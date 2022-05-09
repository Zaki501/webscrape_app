from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import core.crud as crud
import core.schemas as schemas
from api.security import (
    authenticate_user,
    confirm_reset_token,
    create_access_token,
    create_temp_access_token,
)
from core.database import get_db
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES
from limiter import limiter

router = APIRouter(tags=["Auth"], prefix="/api/auth")


@router.post("/login", response_model=schemas.Token)
@limiter.limit("3/minute")
async def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
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


@router.post("/forgot_password_link")
@limiter.limit("3/minute")
async def dfaf(email: str, request: Request, db: Session = Depends(get_db)):
    """Create token w/expiry, post to email

    Sends JWT with email and expiry, secret is user's hashed password
    """
    user = crud.read_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=400, detail="Email doesn't exist")
    jwt_access_token = create_temp_access_token(
        data={"sub": user.email},
        secret=user.hashed_password,
        expires_delta=timedelta(minutes=15),
    )
    return {
        "message": "Reset Code sent to email",
        "email": email,
        "reset_url": f"{request.base_url}api/auth/forgot_password_reset/{jwt_access_token}",
    }


@router.get("/forgot_password_reset/{token}")
@limiter.limit("3/minute")
async def verify_password_reset_token(
    token: str, request: Request, response: Response, db: Session = Depends(get_db)
):
    """Authenticate token, respond with success. Decode JWT and verify"""
    (access_token, _) = confirm_reset_token(token, db)
    response.set_cookie(key="reset_token", value=access_token, httponly=True)
    return {"success": "Cookie created"}


@router.post("/change_password/{}")
async def forgot_password_new_password(
    new_password: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """User enters new password

    After being redirected to change password upon succesful login,
    extract user from browser cookie, if valid change password."""
    token = request.cookies["reset_token"]
    (_, payload) = confirm_reset_token(token, db)
    email = payload["sub"]
    crud.update_user_password(db, email, new_password)
    response.delete_cookie("access_token")
    return (request.cookies["reset_token"], payload)
