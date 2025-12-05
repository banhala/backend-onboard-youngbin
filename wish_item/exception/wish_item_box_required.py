from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class WishItemBoxRequiredException(AblyBaseAPIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "상품을 찜하려면 최소 1개 이상의 찜 서랍이 필요합니다."
    code = "WISH_ITEM_BOX_REQUIRED"

    def __init__(self, message: str | None = None, data: object = None) -> None:
        if message:
            self.message = message
        super().__init__(data=data)
