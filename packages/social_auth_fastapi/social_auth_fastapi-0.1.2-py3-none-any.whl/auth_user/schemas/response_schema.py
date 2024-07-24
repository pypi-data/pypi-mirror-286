#!/usr/bin/env python3
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from ..conf import settings

_ExcludeData = set[int | str] | dict[int | str, Any]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    Unified return model

    .. tip::

        If you don't want to use the custom encoder in ResponseBase, you can use this model,
        and the return data will be automatically parsed and returned through the encoder inside fastapi;
        This return model generates openapi schema documentation

    E.g. ::

        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})

        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})

        @router.get('/test')
        def test() -> ResponseModel:
            res = CustomResponseCode.HTTP_200
            return ResponseModel(code=res.code, msg=res.msg, data={'test': 'test'})
    """

    # TODO: json_encoders Configuration failure: https://github.com/tiangolo/fastapi/discussions/10252
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = 200
    msg: str = 'Request successful'
    data: Any | None = None


class ResponseBase:
    """
    Unified return method

    .. tip::

        The return method in this class will return the ResponseModel model, which exists as a coding style;

    E.g. ::

        @router.get('/test')
        def test() -> ResponseModel:
            return await response_base.success(data={'test': 'test'})
    """

    @staticmethod
    async def __response(*, code, msg, data: Any | None = None) -> ResponseModel:
        """
        The request returns a common method if successful

        :param res: Return messages
        :param data: Return data
        :return:
        """
        return ResponseModel(code=code, msg=msg, data=data)

    async def success(
        self,
        *,
        code=200,
        msg='Request successful',
        data: Any | None = None,
    ) -> ResponseModel:
        return await self.__response(code=code, msg=msg, data=data)

    async def fail(
        self,
        *,
        code=400,
        msg='Bad Request',
        data: Any = None,
    ) -> ResponseModel:
        return await self.__response(code=code, msg=msg, data=data)


response_base = ResponseBase()
