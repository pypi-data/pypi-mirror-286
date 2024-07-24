from typing import Any

from ...base.errors import BaseExceptionMixin


class SSOExceptionError(BaseExceptionMixin):
    code = 400

    def __init__(
        self,
        *,
        msg: str = 'SSO Exception Error',
        data: Any = None,
    ):
        super().__init__(msg=msg, data=data)
