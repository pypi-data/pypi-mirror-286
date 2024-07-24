#!/usr/bin/env python3
from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Query, Path

from ..schemas.response_schema import response_base
from ..schemas.token import GetLoginToken
from ..services.social import SocialService

social_router = APIRouter(prefix="/social", tags=["Social"])


@social_router.get("/{provider}/auth-init")
async def social_auth_url_init(provider: Annotated[str, Path(...)], redirect_uri: Annotated[str, Query()]):
    """Initialize auth and redirect"""
    service = SocialService(provider)
    url = await service.build_auth_url(redirect_uri)
    return await response_base.success(data={"url": url})


@social_router.get("/{provider}/auth")
async def social_auth(provider: Annotated[str, Path(...)],
                      request: Request,
                      redirect_uri: Annotated[str, Query()],
                      code: Annotated[str, Query()],
                      state: Annotated[str, Query()]):
    """Initialize auth and redirect"""
    service = SocialService(provider)
    (
        access_token,
        refresh_token,
        access_expire,
        refresh_expire
    ) = await service.verify_login(request, redirect_uri)
    data = GetLoginToken(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expire_time=access_expire,
        refresh_token_expire_time=refresh_expire
    )
    return await response_base.success(data=data)
