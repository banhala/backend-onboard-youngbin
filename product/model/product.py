from django.db import models

from common.fields import ForceAutoNowDateTimeField


class Product(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name="상품명", max_length=255)
    thumbnail = models.URLField(verbose_name="썸네일 URL", max_length=500)
    price = models.IntegerField(verbose_name="가격")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = ForceAutoNowDateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        db_table = "products"
        verbose_name = "상품"
        verbose_name_plural = "상품"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name
