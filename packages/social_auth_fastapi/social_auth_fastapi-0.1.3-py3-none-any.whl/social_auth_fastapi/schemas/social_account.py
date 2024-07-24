#!/usr/bin/env python3
from typing import Optional, Any

from pydantic import ConfigDict, BaseModel

from ..schemas.user import RegisterUserParam


class SocialAccountSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    login_id: str
    provider: Optional[str] = None
    password: Optional[str] = None
    user_id: Optional[Any] = None


class RegisterSocialAccountParam(SocialAccountSchemaBase):
    pass


class UpdateSocialAccountParam(SocialAccountSchemaBase):
    pass


class RegisterAccountParam(SocialAccountSchemaBase, RegisterUserParam):
    pass
