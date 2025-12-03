from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class MemberInvalidEmailException(AblyBaseAPIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이메일 형식이 올바르지 않습니다."
    code = "INVALID_EMAIL_FORMAT"

    def __init__(self, message: str | None = None, data: object = None) -> None:
        if message:
            self.message = message
        super().__init__(data=data)
