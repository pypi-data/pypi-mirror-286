#!/usr/bin/env python3
import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.t_social_account import SocialAccount
from ..oauth.jwt import get_hash_password
from ..schemas.social_account import RegisterSocialAccountParam, UpdateSocialAccountParam

from .base import CRUDBase


class CRUDSocialAccount(CRUDBase[SocialAccount, RegisterSocialAccountParam, UpdateSocialAccountParam]):

    async def get_by_login_id_and_provider(self, db: AsyncSession, login_id: str, provider: str
                                           ) -> SocialAccount | None:
        user = await db.execute(select(self.model).where(and_(self.model.login_id == login_id,
                                                              self.model.provider == provider)))
        return user.scalars().first()

    async def get_by_user_id_and_provider(self, db: AsyncSession, user_id: int, provider: str
                                          ) -> SocialAccount | None:
        user = await db.execute(select(self.model).where(and_(self.model.user_id == user_id,
                                                              self.model.provider == provider)))
        return user.scalars().first()

    async def create(self, db: AsyncSession, obj: RegisterSocialAccountParam, **kwargs) -> SocialAccount:
        if obj.password:
            obj.password = await get_hash_password(obj.password)
        else:
            obj.password = await get_hash_password(uuid.uuid4().hex)

        dict_obj = obj.model_dump()
        new_user = self.model(**dict_obj)
        db.add(new_user)
        await db.flush()
        return new_user


SocialAccountDao: CRUDSocialAccount = CRUDSocialAccount(SocialAccount)
