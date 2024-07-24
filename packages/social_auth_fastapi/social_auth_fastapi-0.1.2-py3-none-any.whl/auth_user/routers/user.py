#!/usr/bin/env python3

from fastapi import APIRouter

from ..schemas.response_schema import response_base
from ..schemas.social_account import RegisterAccountParam
from ..services.user import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post(path='/register', summary='Registration')
async def register_user(obj: RegisterAccountParam):
    data = await UserService().register_user(obj=obj)
    return await response_base.success(data=data)
