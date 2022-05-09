from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import core.crud as crud
import core.schemas as schemas
from api.security import (
    authenticate_reset_token,
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


@router.post("/forgot_password_link")
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

    # return {"access_token": jwt_access_token, "token_type": "bearer"}

    # hash with current pass hash? this method doesnt require a reset pass database
    # email hashed with current pass
    # if current pass changes, signature becomes invalid, so can only be used once
    # user receives email and
    return {
        "message": "Reset Code sent to email",
        "email": email,
        "reset_url": f"{request.base_url}api/auth/forgot_password_reset/{jwt_access_token}",
    }


@router.get("/forgot_password_reset/{token}")
async def dfg(token: str, response: Response, db: Session = Depends(get_db)):
    # = Depends(reset_pass_jwt_check)
    """Authenticate token, respond with success

    Decode JWT and verify"""
    # try:
    #     # decode/verify token
    #     # respond with success (or acces token?) if it works
    #     pass
    # except:
    #     raise HTTPException(status_code=400, detail="Invalid url, already used")
    # pass

    # user = confirm_reset_token(token, db)
    # return {"token": token, "user" : user}
    # (user, token) = data
    # https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
    # https://testdriven.io/blog/fastapi-jwt-auth/#jwt-authentication

    (access_token, payload) = confirm_reset_token(token, db)
    response.set_cookie(key="reset_token", value=access_token, httponly=True)
    return {"success": "Cookie created"}


@router.post("/change_password/{}")
async def sdsds(
    new_password: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """User enters new password

    After being redirected to change password upon succesful login,
    extract user from browser cookie, if valid change password."""
    token = request.cookies["reset_token"]
    # verify token
    (_, payload) = confirm_reset_token(token, db)
    email = payload["sub"]
    # update user passwrod
    crud.update_user_password(db, email, new_password)
    # delete cookie
    response.delete_cookie("access_token")
    return (request.cookies["reset_token"], payload)


@router.get("/del_cookie")
async def dfsfs(response: Response):
    response.delete_cookie("access_token")
    return {"success": "Cookie Deleted"}


@router.post("/register", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    db_user = crud.read_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# @router.post("/forgot_password")
# async def send_token_to_email(
#     email: str, request: Request, db: Session = Depends(get_db)
# ):
#     # create token, store in ResetPassword
#     # send token to users email, as URL

#     # user enters email for forgotten password
#     # if user doesnt exist, raise error
#     # create token for user, send in email
#     # hash token and add to db

#     # current tokens are security risk? they are the same each minute
#     # rate? limit users password guesses
#     # check if reset request already sent

#     # totp tokens are time-based, and independent of client and server
#     # look into google auth

#     # if user not in users table, return error
#     # if user in resetpassword table, delete them

#     user = crud.read_user_by_email(db, email)
#     if not user:
#         raise HTTPException(status_code=400, detail="Email doesn't exist")
#     if crud.read_password_reset(db, email) is not None:
#         crud.delete_password_reset(db, email)
#     token = generate_token()
#     crud.create_password_reset(db, email, token)
#     return {
#         "message": "Reset Code sent to email",
#         "token": token,
#         "email": email,
#         "url": f"{request.base_url}",
#         "reset_url": f"{request.base_url}api/auth/authenticate_token/{email}&{token}",
#     }


@router.get("/authenticate_token/{email}&{token}")
@limiter.limit("3/minute")
async def confirm_token(
    request: Request,
    # new_password: str,
    user: schemas.ResetToken = Depends(authenticate_reset_token),
    db: Session = Depends(get_db),
):
    """Rate limited - 3 attempts per minute"""
    # resend token endpoint
    # new_password

    # match email and token to db
    # user = crud.read_password_reset(db, email)
    # if user is None:
    #     raise HTTPException(
    #         status_code=400, detail="Link already used, request another"
    #     )

    # if not verify_hash(token, user.token_hash):
    #     raise HTTPException(status_code=400, detail="Invalid hash")

    # if is_expired(user.expiration):
    #     raise HTTPException(status_code=400, detail="Link is expired, request another")

    # if user.token_used:
    #     raise HTTPException(status_code=400, detail="Token Used already")

    # ## After token is verified, ask for another input. depedency injection??

    # crud.update_user_password(db, email, new_password)
    # crud.update_password_reset(db, email)

    # app.post, {email/token} = depends(token auth)
    # https://stackoverflow.com/questions/62279710/fastapi-variable-query-parameters
    # https://lifesaver.codes/answer/what-s-the-reset-password-flow-604

    # make token check a dependency -> return email?
    # if failed, show error text
    # if success, redirect to pass reset (front end detects success, shows UI for pass reset)
    # https://stytch.com/blog/forget-the-password-reset-flow-as-you-know-it/

    # redirect to app.post(reset_password/)
    # use email from authneticated reset token, allow user to change password

    # https://supertokens.com/blog/implementing-a-forgot-password-flow

    # https://melodiessim.netlify.app/Reset%20Password%20Flow%20Using%20JWT/
    return {
        "success": "success",
        # "email": user.email,
        # "token": user.token,
        "user": user,
        # "new_pass": "",
        "url": request.url._url,
    }


# add scope to this auth, or use depends?

# @router.post("/authenticate_token/{email}&{token}")
# async def reset_password(new_password: str, db: Session = Depends(get_db)):
#     """After the token is confirmed, it will route to this endpoint"""
#     # redirect to another endpoin, chnge query params in redirect
#     pass
