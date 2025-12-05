from typing import List, Tuple

from product.domain.product_repository import ProductRepository
from product.exception.product_not_found import ProductNotFoundException
from wish_item.domain.wish_item_repository import WishItemRepository
from wish_item.exception.wish_item_already_exist import WishItemAlreadyExistException
from wish_item.exception.wish_item_box_required import WishItemBoxRequiredException
from wish_item.exception.wish_item_not_found import WishItemNotFoundException
from wish_item.model.wish_item import WishItem
from wish_item_box.domain.wish_item_box_repository import WishItemBoxRepository
from wish_item_box.exception.wish_item_box_not_found import WishItemBoxNotFoundException


class WishItemService:
    def __init__(
        self,
        wish_item_repository: WishItemRepository,
        wish_item_box_repository: WishItemBoxRepository,
        product_repository: ProductRepository,
    ) -> None:
        self.wish_item_repository = wish_item_repository
        self.wish_item_box_repository = wish_item_box_repository
        self.product_repository = product_repository

    def add_wish_item(
        self,
        member_id: int,
        wish_item_box_id: int,
        product_id: int,
    ) -> WishItem:
        if self.wish_item_box_repository.count_by_member_id(member_id) == 0:
            raise WishItemBoxRequiredException()

        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise ProductNotFoundException(
                f"상품을 찾을 수 없습니다. product_id: {product_id}"
            )

        wish_item_box = self.wish_item_box_repository.find_by_id(wish_item_box_id)
        if not wish_item_box:
            raise WishItemBoxNotFoundException(
                f"찜 서랍을 찾을 수 없습니다. wish_item_box_id: {wish_item_box_id}"
            )

        if wish_item_box.member_id != member_id:
            raise WishItemBoxNotFoundException("접근 권한이 없습니다.")

        if self.wish_item_repository.exists_by_member_and_product(
            member_id, product_id
        ):
            raise WishItemAlreadyExistException(product_id)

        return self.wish_item_repository.save(
            wish_item_box_id, product_id, product.name, product.price
        )

    def remove_wish_item(self, member_id: int, wish_item_id: int) -> None:
        wish_item = self.wish_item_repository.find_by_id(wish_item_id)
        if not wish_item:
            raise WishItemNotFoundException(
                f"찜 상품을 찾을 수 없습니다. wish_item_id: {wish_item_id}"
            )

        if wish_item.wish_item_box.member_id != member_id:
            raise WishItemNotFoundException("접근 권한이 없습니다.")

        self.wish_item_repository.delete(wish_item_id)

    def get_wish_items(
        self, member_id: int, wish_item_box_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[WishItem], int]:
        # 페이지네이션 파라미터 유효성 검사
        if page < 1:
            raise ValueError("페이지 번호는 1 이상이어야 합니다.")
        if page_size < 1 or page_size > 100:
            raise ValueError("페이지 크기는 1에서 100 사이여야 합니다.")

        # 찜 서랍 존재 여부 및 권한 확인
        wish_item_box = self.wish_item_box_repository.find_by_id(wish_item_box_id)
        if not wish_item_box:
            raise WishItemBoxNotFoundException(
                f"찜 서랍을 찾을 수 없습니다. wish_item_box_id: {wish_item_box_id}"
            )

        if wish_item_box.member_id != member_id:
            raise WishItemBoxNotFoundException("접근 권한이 없습니다.")

        return self.wish_item_repository.find_by_wish_item_box_id(
            wish_item_box_id, page, page_size
        )
