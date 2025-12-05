from __future__ import annotations

from typing import List

from django.core.paginator import Paginator

from wish_item_box.model.wish_item_box import WishItemBox


class WishItemBoxRepository:

    def find_by_id(self, wish_item_box_id: int) -> WishItemBox | None:
        try:
            return WishItemBox.objects.get(id=wish_item_box_id)
        except WishItemBox.DoesNotExist:
            return None

    def find_by_member_id(
        self, member_id: int, page: int = 1, page_size: int = 20
    ) -> tuple[List[WishItemBox], int]:
        queryset = WishItemBox.objects.filter(member_id=member_id)
        total_count = queryset.count()

        paginator = Paginator(queryset, page_size)
        wish_item_boxes = list(paginator.get_page(page).object_list)

        return wish_item_boxes, total_count

    def exists_by_member_and_name(self, member_id: int, name: str) -> bool:
        return WishItemBox.objects.filter(member_id=member_id, name=name).exists()

    def save(self, member_id: int, name: str) -> WishItemBox:
        return WishItemBox.objects.create(member_id=member_id, name=name)

    def delete(self, wish_item_box_id: int) -> bool:
        try:
            wish_item_box = WishItemBox.objects.get(id=wish_item_box_id)
            wish_item_box.delete()
            return True
        except WishItemBox.DoesNotExist:
            return False

    def count_by_member_id(self, member_id: int) -> int:
        return WishItemBox.objects.filter(member_id=member_id).count()
