from django.db import models

from common.fields import ForceAutoNowDateTimeField
from wish_item_box.model.wish_item_box import WishItemBox


class WishItem(models.Model):

    id = models.BigAutoField(primary_key=True)
    wish_item_box = models.ForeignKey(
        WishItemBox,
        on_delete=models.CASCADE,
        verbose_name="찜 서랍",
        related_name="wish_items",
        db_constraint=False,
    )
    product_id: int = models.BigIntegerField(verbose_name="상품 ID")
    product_name: str = models.CharField(verbose_name="상품명", max_length=255)
    product_price: int = models.IntegerField(verbose_name="상품 가격")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = ForceAutoNowDateTimeField(auto_now=True)

    class Meta:
        db_table = "wish_items"
        verbose_name = "찜 상품"
        verbose_name_plural = "찜 상품"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.wish_item_box.name} - {self.product_name}"
