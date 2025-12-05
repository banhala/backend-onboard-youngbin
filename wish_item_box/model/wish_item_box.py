from django.db import models

from common.fields import ForceAutoNowDateTimeField
from member.model.member import Member


class WishItemBox(models.Model):

    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="회원",
        related_name="wish_item_boxes",
        db_constraint=False,
    )
    name: str = models.CharField(verbose_name="찜 서랍 이름", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = ForceAutoNowDateTimeField(auto_now=True)

    class Meta:
        db_table = "wish_item_boxes"
        verbose_name = "찜 서랍"
        verbose_name_plural = "찜 서랍"
        constraints = [
            models.UniqueConstraint(
                fields=["member", "name"], name="unique_member_wish_item_box_name"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.member.email} - {self.name}"
