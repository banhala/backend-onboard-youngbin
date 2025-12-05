from __future__ import annotations

from rest_framework import status

from common.exception.ably_api_exception import AblyBaseAPIException


class WishItemAlreadyExistException(AblyBaseAPIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 찜한 상품입니다."
    code = "WISH_ITEM_ALREADY_EXISTS"

    def __init__(self, product_id: int | None = None, data: object = None) -> None:
        if product_id:
            self.message = f"이미 찜한 상품입니다. product_id: {product_id}"
        super().__init__(data=data)
