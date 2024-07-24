#!/usr/bin/env python3
from typing import Any

from fastapi import Request, Response
from loguru import logger
from sqlalchemy.exc import ArgumentError
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection

from core.common import jwt
from core.exception.errors import RequestError, TokenError
from core.utils.serializers import MsgSpecJSONResponse


class _AuthenticationError(AuthenticationError):
    """Override internal authentication error classes"""

    def __init__(self, *, code: int = None, msg: str = None, headers: dict[str, Any] | None = None):
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT Authentication middleware"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: _AuthenticationError) -> Response:
        """Override internal authentication error handling"""
        return MsgSpecJSONResponse(content={'code': exc.code, 'msg': exc.msg, 'data': None}, status_code=exc.code)

    async def authenticate(self, request: Request):
        auth = request.headers.get('Authorization')

        if not auth:
            return

        try:
            scheme, token = auth.split()
            if scheme.lower() != 'bearer':
                return
        except ValueError:
            token = auth
        try:
            sub = await jwt.jwt_authentication(token)
            # user = await AuthService().get_current_user(data=sub)
            user = None
        except TokenError as exc:
            raise _AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except ArgumentError as earg:
            raise RequestError(msg=earg.args[0])
        except Exception as e:
            logger.error(e)
            raise _AuthenticationError(
                code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'An unknown error has occurred on the server.')
            )

        # Note that this return uses a non-standard mode, so when authentication passes,
        # some standard features will be lost
        # Please see the standard return mode：https://www.starlette.io/authentication/
        return AuthCredentials(['authenticated']), user
