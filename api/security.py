import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.crud import read_password_reset, read_user_by_email
from core.database import get_db
from core.schemas import ResetToken, TokenData, User
from core.security import ALGORITHM, SECRET_KEY, is_expired, oauth2_scheme, verify_hash


def authenticate_user(db: Session, email: str, password: str):
    """Verify email and password match"""
    user = read_user_by_email(db, email)
    if not user:
        return False
    if not verify_hash(password, user.hashed_password):
        return False
    return user


#######################################################

# data = {email, token = generate_token()}
# encode data as jwt: create_access_token(data, time_delta))
# decode data:


def create_temp_access_token(data: dict, secret: str, expires_delta: timedelta):
    """For pass reset only

    Users current pass hash used as secret to generate a JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return encoded_jwt


def verify_temp_access_token(db: Session = Depends(get_db)):
    """"""


#######################################################

# Encode JWT token


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#######################################################

# Authorisation methods:
# Decode users JWT token, and then validate credentials against database


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = read_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_reset_token(
    email: str,
    token: str,
    db: Session = Depends(get_db),
) -> ResetToken:
    user_pass_reset = read_password_reset(db, email)
    if user_pass_reset is None:
        raise HTTPException(
            status_code=400, detail="Link already used, request another"
        )

    if not verify_hash(token, user_pass_reset.token_hash):
        raise HTTPException(status_code=400, detail="Invalid hash")

    if is_expired(user_pass_reset.expiration):
        raise HTTPException(status_code=400, detail="Link is expired, request another")

    if user_pass_reset.token_used:
        raise HTTPException(status_code=400, detail="Token Used already")

    return ResetToken(email=email, token=token)


def confirm_reset_token(token: str, db: Session):
    # if this is async it throws an error for some reason
    """After user clicks reset link, attempt to confirm it

    Confirm by checking the token isnt expired, and that the
    JWT token is verified (secret should be current password,
    if its invalid then it must have been changed already
    )
    Return user if confirmed"""

    try:
        unverified_payload = jwt.get_unverified_claims(token)
    except JWTError:
        raise HTTPException(status_code=400, detail="unverified jwt -  ERROR)")

    if time.time() > (unverified_payload["exp"]):
        raise HTTPException(status_code=400, detail="Token is expired")
    user = read_user_by_email(db, unverified_payload["sub"])

    if user is None:
        raise HTTPException(status_code=400, detail="User no longer exists")
    try:
        verified_payload = jwt.decode(
            token, user.hashed_password, algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=400, detail="Token is Invalid (JWT verification error)"
        )

    if not verified_payload:
        raise HTTPException(status_code=400, detail="Invalid token (any reason)")
    # user verified token, query current user
    # return (user, token)

    return (token, verified_payload)


def abc():
    """Extract user from access token in Cookie

    Check signature and expiry"""
    pass
