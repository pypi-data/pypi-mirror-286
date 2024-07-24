from sqlalchemy.ext.asyncio import AsyncSession

from ..conf import settings
from ..base import errors
from ..cruds.crud_social_account import SocialAccountDao
from ..schemas.social_account import RegisterSocialAccountParam, RegisterAccountParam


class UserService:
    def __init__(self):
        self.provider = 'password'

    async def register_user(self, obj: RegisterAccountParam, **kwargs):
        async with settings.DB_SESSION() as db:
            account = await SocialAccountDao.get_by_login_id_and_provider(
                db=db, login_id=obj.login_id,
                provider=self.provider)
            obj.provider = self.provider

            if account:
                raise errors.UnprocessedContentError(msg='Login ID is already registered.')

            account = await self.create_new_account(db, obj)
            await db.commit()

        return dict(user_id=account.user_id)

    async def create_new_account(self, db: AsyncSession, account_req: RegisterAccountParam):
        register_account = RegisterSocialAccountParam(
            login_id=account_req.login_id,
            user_id=account_req.user_id,
            provider=account_req.provider,
            password=account_req.password
        )
        account = await SocialAccountDao.create(db, register_account)
        return account
