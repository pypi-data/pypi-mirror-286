from pydantic import ConfigDict, BaseModel

from ..oauth.timezone import Timestamp


class AccessTokenBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: Timestamp


class GetLoginToken(AccessTokenBase):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: Timestamp
