#!/usr/bin/env python3
"""
Global business exception class

When business code executes abnormally, you can use raise xxxError to trigger internal errors.
It implements exceptions with background tasks as much as possible, but it does not apply to **custom response status codes**
If you are required to use **custom response status code**, you can return directly by return await response_base.fail(res=CustomResponseCode.xxx)
"""  # noqa: E501

from typing import Any

from fastapi import HTTPException
from starlette.background import BackgroundTask

from core.common.messages import messages as _
from core.response.response_code import CustomErrorCode, StandardResponseCode


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None, background: BackgroundTask | None = None):
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background


class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None):
        super().__init__(status_code=code, detail=msg, headers=headers)


class CustomError(BaseExceptionMixin):
    def __init__(self, *, error: CustomErrorCode, data: Any = None, background: BackgroundTask | None = None):
        self.code = error.code
        super().__init__(msg=error.msg, data=data, background=background)


class RequestError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_400

    def __init__(self, *, msg: str = _('Bad Request'), data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class ForbiddenError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_403

    def __init__(self, *, msg: str = _('Forbidden'), data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class NotFoundError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_404

    def __init__(self, *, msg: str = _('Not Found'), data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class UnprocessedContentError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_422

    def __init__(
        self, *, msg: str = _('Unprocessed Content'), data: Any = None, background: BackgroundTask | None = None
    ):
        super().__init__(msg=msg, data=data, background=background)


class ServerError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_500

    def __init__(
        self, *, msg: str = _('Internal Server Error'), data: Any = None, background: BackgroundTask | None = None
    ):
        super().__init__(msg=msg, data=data, background=background)


class GatewayError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_502

    def __init__(self, *, msg: str = _('Bad Gateway'), data: Any = None, background: BackgroundTask | None = None):
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_401

    def __init__(
        self, *, msg: str = _('Permission Denied'), data: Any = None, background: BackgroundTask | None = None
    ):
        super().__init__(msg=msg, data=data, background=background)


class TokenError(HTTPError):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Not Authenticated', headers: dict[str, Any] | None = None):
        super().__init__(code=self.code, msg=_(msg), headers=headers or {'WWW-Authenticate': 'Bearer'})

class SSOExceptionError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_400

    def __init__(
        self,
        *,
        msg: str = _('SSO Exception Error'),
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        super().__init__(msg=msg, data=data, background=background)

class S3BucketExceptionError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_500

    def __init__(
        self,
        *,
        msg: str = _('S3 Bucket Exception'),
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        super().__init__(msg=msg, data=data, background=background)

class SQSExceptionError(BaseExceptionMixin):
    code = StandardResponseCode.HTTP_500

    def __init__(
        self,
        *,
        msg: str = _('SQS Exception Error'),
        data: Any = None,
        background: BackgroundTask | None = None,
    ):
        super().__init__(msg=msg, data=data, background=background)