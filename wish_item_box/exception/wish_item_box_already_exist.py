from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class WishItemBoxAlreadyExistException(AblyBaseAPIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 존재하는 찜 서랍 이름입니다."
    code = "WISH_ITEM_BOX_ALREADY_EXISTS"

    def __init__(self, name: str | None = None, data: object = None) -> None:
        if name:
            self.message = f"이미 존재하는 찜 서랍 이름입니다: {name}"
        super().__init__(data=data)
