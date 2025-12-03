from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class MemberAuthenticationException(AblyBaseAPIException):

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "인증에 실패했습니다."
    code = "AUTHENTICATION_FAILED"

    def __init__(self, message: str | None = None, data: object = None) -> None:
        if message:
            self.message = message
        super().__init__(data=data)
