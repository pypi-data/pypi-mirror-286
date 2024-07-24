from ..oauth import jwt
from ..base import errors
from .. import settings
from ..cruds.crud_social_account import SocialAccountDao
from ..schemas.auth import LoginParam


class AuthService:
    def __init__(self, provider='password'):
        self.provider = provider

    async def login(self, request: LoginParam):
        async with settings.DB_SESSION() as db:
            account = await SocialAccountDao.get_by_login_id_and_provider(
                db=db, login_id=request.username,
                provider=self.provider)

            await self.validate_login(account, request)
            access_token, access_token_expire_time = await jwt.create_access_token(
                str(account.user_id),
                provider=self.provider)
            refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                str(account.user_id),
                access_token_expire_time,
                provider=self.provider
            )
            return (
                access_token,
                refresh_token,
                access_token_expire_time,
                refresh_token_expire_time
            )

    @staticmethod
    async def validate_login(current_account, data):
        if not current_account:
            raise errors.NotFoundError(msg='Please enter a valid username or password')
        else:
            if data.password and not await jwt.password_verify(
                data.password, current_account.password
            ):
                raise errors.AuthorizationError(msg='Please enter a valid username or password')
