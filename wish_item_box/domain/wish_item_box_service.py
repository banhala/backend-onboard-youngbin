from typing import List, Tuple

from wish_item_box.domain.wish_item_box_repository import WishItemBoxRepository
from wish_item_box.exception.wish_item_box_already_exist import (
    WishItemBoxAlreadyExistException,
)
from wish_item_box.exception.wish_item_box_not_found import WishItemBoxNotFoundException
from wish_item_box.model.wish_item_box import WishItemBox


class WishItemBoxService:
    def __init__(self, wish_item_box_repository: WishItemBoxRepository) -> None:
        self.wish_item_box_repository = wish_item_box_repository

    def create_wish_item_box(self, member_id: int, name: str) -> WishItemBox:
        if not name:
            raise ValueError("찜 서랍 이름은 필수입니다.")

        if self.wish_item_box_repository.exists_by_member_and_name(member_id, name):
            raise WishItemBoxAlreadyExistException(name)

        return self.wish_item_box_repository.save(member_id, name)

    def delete_wish_item_box(self, member_id: int, wish_item_box_id: int) -> None:
        wish_item_box = self.wish_item_box_repository.find_by_id(wish_item_box_id)
        if not wish_item_box:
            raise WishItemBoxNotFoundException(
                f"찜 서랍을 찾을 수 없습니다. wish_item_box_id: {wish_item_box_id}"
            )

        if wish_item_box.member_id != member_id:
            raise WishItemBoxNotFoundException("접근 권한이 없습니다.")

        self.wish_item_box_repository.delete(wish_item_box_id)

    def get_wish_item_boxes(
        self, member_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[WishItemBox], int]:
        # 페이지네이션 파라미터 유효성 검사
        if page < 1:
            raise ValueError("페이지 번호는 1 이상이어야 합니다.")
        if page_size < 1 or page_size > 100:
            raise ValueError("페이지 크기는 1에서 100 사이여야 합니다.")

        return self.wish_item_box_repository.find_by_member_id(
            member_id, page, page_size
        )
