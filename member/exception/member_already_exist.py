from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class MemberAlreadyExistException(AblyBaseAPIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 존재하는 회원입니다."
    code = "MEMBER_ALREADY_EXISTS"

    def __init__(self, email: str | None = None, data: object = None) -> None:
        if email:
            self.message = f"이미 존재하는 이메일입니다: {email}"
        super().__init__(data=data)
