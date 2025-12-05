from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class WishItemBoxNotFoundException(AblyBaseAPIException):

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "찜 서랍을 찾을 수 없습니다."
    code = "WISH_ITEM_BOX_NOT_FOUND"

    def __init__(self, message: str | None = None, data: object = None) -> None:
        if message:
            self.message = message
        super().__init__(data=data)
