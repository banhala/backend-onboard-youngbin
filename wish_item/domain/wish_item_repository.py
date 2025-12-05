from __future__ import annotations

from typing import List

from django.core.paginator import Paginator

from wish_item.model.wish_item import WishItem


class WishItemRepository:

    def find_by_id(self, item_id: int) -> WishItem | None:
        try:
            return WishItem.objects.select_related("wish_item_box").get(id=item_id)
        except WishItem.DoesNotExist:
            return None

    def find_by_wish_item_box_id(
        self, wish_item_box_id: int, page: int = 1, page_size: int = 20
    ) -> tuple[List[WishItem], int]:
        queryset = WishItem.objects.filter(wish_item_box_id=wish_item_box_id)
        total_count = queryset.count()

        paginator = Paginator(queryset, page_size)
        items = list(paginator.get_page(page).object_list)

        return items, total_count

    def exists_by_member_and_product(self, member_id: int, product_id: int) -> bool:
        return WishItem.objects.filter(
            wish_item_box__member_id=member_id, product_id=product_id
        ).exists()

    def save(
        self,
        wish_item_box_id: int,
        product_id: int,
        product_name: str,
        product_price: int,
    ) -> WishItem:
        return WishItem.objects.create(
            wish_item_box_id=wish_item_box_id,
            product_id=product_id,
            product_name=product_name,
            product_price=product_price,
        )

    def delete(self, item_id: int) -> bool:
        try:
            item = WishItem.objects.get(id=item_id)
            item.delete()
            return True
        except WishItem.DoesNotExist:
            return False
