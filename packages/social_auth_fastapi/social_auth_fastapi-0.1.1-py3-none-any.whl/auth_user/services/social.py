from typing import Optional

from fastapi import Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from .. import settings
from ..oauth import jwt
from ..social.sso.errors import SSOExceptionError
from ..cruds.crud_social_account import SocialAccountDao
from ..schemas.social_account import RegisterSocialAccountParam
from ..social.services.github import GithubService
from ..social.services.google import GoogleService
from ..social.sso.constant import ProviderEnum


class SocialService:
    def __init__(self, provider):
        self.provider = provider
        self.sso_service = self.__init_sso__by_provider()

    def __init_sso__by_provider(self):
        match self.provider:
            case ProviderEnum.GOOGLE:
                return GoogleService()
            case ProviderEnum.GITHUB:
                return GithubService()
            case _:
                raise SSOExceptionError(msg='Provider invalid')

    async def build_auth_url(self, redirect_uri: str):
        return await self.sso_service.build_auth_url(redirect_uri)

    async def verify_login(self, request: Request, redirect_uri: Optional[str] = None):
        try:
            user_profile = await self.sso_service.sso.verify_and_process(request, redirect_uri=redirect_uri)
            async with settings.DB_SESSION() as db:
                account = await SocialAccountDao.get_by_login_id_and_provider(
                    db=db, login_id=user_profile.id,
                    provider=user_profile.provider)
                if account is None:
                    account = await self.create_new_account(db, user_profile.id, None, user_profile.provider)

                access_token, access_token_expire_time = await jwt.create_access_token(
                    str(account.login_id),
                    provider=user_profile.provider)
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(account.login_id),
                    access_token_expire_time,
                    provider=user_profile.provider
                )
                await db.commit()
                return (
                    access_token,
                    refresh_token,
                    access_token_expire_time,
                    refresh_token_expire_time
                )
        except Exception as e:
            logger.error(e)
            raise e

    async def create_new_account(self, db: AsyncSession, login_id, user_id, provider):
        register_account = RegisterSocialAccountParam(
            login_id=login_id,
            provider=provider,
            user_id=user_id
        )
        account = await SocialAccountDao.create(db, register_account)
        return account
