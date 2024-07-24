#!/usr/bin/env python3
"""
Global business exception class

When business code executes abnormally, you can use raise xxxError to trigger internal errors.
It implements exceptions with background tasks as much as possible, but it does not apply to **custom response status codes**
If you are required to use **custom response status code**, you can return directly by return await response_base.fail(res=CustomResponseCode.xxx)
"""  # noqa: E501

from typing import Any

from fastapi import HTTPException

from .error_codes import StandardResponseCode


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None):
        self.msg = msg
        self.data = data


class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None):
        super().__init__(status_code=code, detail=msg, headers=headers)


class RequestError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_400

    def __init__(self, *, msg: str = 'Bad Request', data: Any = None):
        super().__init__(msg=msg, data=data)


class ForbiddenError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_403

    def __init__(self, *, msg: str = 'Forbidden', data: Any = None):
        super().__init__(msg=msg, data=data)


class NotFoundError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_404

    def __init__(self, *, msg: str = 'Not Found', data: Any = None):
        super().__init__(msg=msg, data=data)


class UnprocessedContentError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_422

    def __init__(
        self, *, msg: str = 'Unprocessed Content', data: Any = None
    ):
        super().__init__(msg=msg, data=data)


class ServerError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_500

    def __init__(
        self, *, msg: str = 'Internal Server Error', data: Any = None
    ):
        super().__init__(msg=msg, data=data)


class GatewayError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_502

    def __init__(self, *, msg: str = 'Bad Gateway', data: Any = None):
        super().__init__(msg=msg, data=data)


class AuthorizationError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_401

    def __init__(
        self, *, msg: str = 'Permission Denied', data: Any = None
    ):
        super().__init__(msg=msg, data=data)


class TokenError(HTTPError):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Not Authenticated', headers: dict[str, Any] | None = None):
        super().__init__(code=self.code, msg=msg, headers=headers or {'WWW-Authenticate': 'Bearer'})
