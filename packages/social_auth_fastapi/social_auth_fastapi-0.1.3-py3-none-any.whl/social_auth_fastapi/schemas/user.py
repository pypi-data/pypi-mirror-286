#!/usr/bin/env python3
from pydantic import ConfigDict, BaseModel


class UserSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str | None = None
    picture: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class RegisterUserParam(UserSchemaBase):
    pass


class UpdateUserParam(UserSchemaBase):
    pass


class CurrentUserInfo(UserSchemaBase):
    pass
