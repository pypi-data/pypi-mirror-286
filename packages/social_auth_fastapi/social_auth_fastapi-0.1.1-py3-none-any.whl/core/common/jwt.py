#!/usr/bin/env python3
from datetime import datetime, timedelta
from typing import Tuple

from asgiref.sync import sync_to_async
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt as jose_jwt
from passlib.context import CryptContext

from conf import settings
from core.common.messages import messages as _
from core.exception.errors import AuthorizationError, TokenError
from core.utils.timezone import DatetimeUTC, timezone


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail=_("Invalid authentication scheme."))

            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail=_("Invalid token or expired token."))

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail=_("Invalid authorization code."))

    async def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = await jwt_decode(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = JWTBearer()


@sync_to_async
def get_hash_password(password: str) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :return:
    """
    return pwd_context.hash(password)


@sync_to_async
def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password verification

    :param plain_password: The password to verify
    :param hashed_password: The hash ciphers to compare
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(sub: str, expires_delta: timedelta | None = None, **kwargs) -> tuple[str, DatetimeUTC]:
    """
    Generate encryption token

    :param sub: The subject/userid of the JWT
    :param expires_delta: Increased expiry time
    :return:
    """
    if expires_delta:
        expire = timezone.now() + expires_delta
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)

    multi_login = kwargs.pop('multi_login', None)
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    token = jose_jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    return token, expire


async def create_refresh_token(sub: str, expire_time: DatetimeUTC | None = None, **kwargs) -> tuple[str, DatetimeUTC]:
    """
    Generate encryption refresh token, only used to create a new token

    :param sub: The subject/userid of the JWT
    :param expire_time: expiry time
    :return:
    """
    if expire_time:
        expire = expire_time + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
        expire_datetime = timezone.f_datetime(expire)
        current_datetime = timezone.now()

        if expire_datetime < current_datetime:
            raise TokenError(msg=_('The token is invalid or has expired'))

    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)

    multi_login = kwargs.pop('multi_login', None)
    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    refresh_token = jose_jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    return refresh_token, expire


async def create_new_token(sub: str, token: str, refresh_token: str, **kwargs) -> tuple[str, str, datetime, datetime]:
    """
    Generate new token

    :param sub:
    :param token
    :param refresh_token:
    :return:
    """

    new_access_token, new_access_token_expire_time = await create_access_token(sub, **kwargs)
    new_refresh_token, new_refresh_token_expire_time = await create_refresh_token(sub, **kwargs)

    return new_access_token, new_refresh_token, new_access_token_expire_time, new_refresh_token_expire_time


@sync_to_async
def get_token(request: Request) -> str:
    """
    Get token for request header

    :return:
    """
    authorization = request.headers.get('Authorization') or request.cookies.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg=_('The token is invalid or has expired'))

    return token


@sync_to_async
def jwt_decode(token: str) -> Tuple:
    """
    Decode token

    :param token:
    :return:
    """
    try:
        payload = jose_jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        user_id = int(payload.get('sub'))
        if not user_id:
            raise TokenError(msg=_('The token is invalid or has expired'))

        provider = payload.get('provider')
    except jose_jwt.ExpiredSignatureError:
        raise TokenError(msg=_('The token is invalid or has expired'))
    except (jose_jwt.JWTError, Exception):
        raise TokenError(msg=_('The token is invalid or has expired'))
    return user_id, provider


async def jwt_authentication(token: str) -> dict[str, int]:
    """
    JWT authentication

    :param token:
    :param jwt_type:
    :return:
    """
    user_id, provider = await jwt_decode(token)
    return {'sub': user_id, 'provider': provider}


async def jwt_encryption_token(
    payload: dict,
    expired_time: int | None = None,  # seconds
) -> tuple[str, datetime]:
    """
    Generate encryption token
    """
    if expired_time:
        expire = timezone.now() + timedelta(seconds=expired_time)
        expire_seconds = expired_time
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS

    token = jose_jwt.encode(payload, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)

    return token, expire


async def jwt_decryption_token(token: str) -> dict:
    """
    Decode token
    """
    try:
        payload = jose_jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
    except jose_jwt.ExpiredSignatureError:
        raise TokenError(msg=_('The token is invalid or has expired'))
    except (jose_jwt.JWTError, Exception):
        raise TokenError(msg=_('The token is invalid or has expired'))

    return payload


@sync_to_async
def superuser_verify(request: Request) -> bool:
    """
    Verify the current user permissions through token

    :param request:
    :return:
    """
    is_superuser = request.user.is_superuser
    if not is_superuser:
        raise AuthorizationError(msg=_('No authentication credentials were provided.'))

    if not request.user.is_staff:
        raise AuthorizationError(msg=_('This administrator has been banned from background management operations'))

    return is_superuser


# JWT authorizes dependency injection, which can be used if the interface only
# needs to provide a token instead of RBAC permission control
DependsJwtAuth = Depends(oauth2_schema)
