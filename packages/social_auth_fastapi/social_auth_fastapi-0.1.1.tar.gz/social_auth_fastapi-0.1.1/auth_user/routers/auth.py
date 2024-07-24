#!/usr/bin/env python3

from fastapi import APIRouter

from ..schemas.auth import LoginParam
from ..schemas.response_schema import response_base
from ..schemas.token import GetLoginToken
from ..services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(path='/login', summary='auth')
async def user_auth(login_request: LoginParam):
    (
        access_token,
        refresh_token,
        access_expire,
        refresh_expire
    ) = await AuthService().login(login_request)

    data = GetLoginToken(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expire_time=access_expire,
        refresh_token_expire_time=refresh_expire
    )
    return await response_base.success(data=data)
