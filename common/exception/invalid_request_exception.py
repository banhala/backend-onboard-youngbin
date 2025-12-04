from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class InvalidRequestException(AblyBaseAPIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "잘못된 요청입니다."

    def __init__(
        self, message: str | None = None, code: str | None = None, data: object = None
    ) -> None:
        if message:
            self.message = message
        if code:
            self.code = code
        super().__init__(data=data)
