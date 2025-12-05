from rest_framework import serializers

from wish_item.model.wish_item import WishItem


class WishItemResponseDTO(serializers.ModelSerializer):
    wish_item_box_id = serializers.IntegerField(
        source="wish_item_box.id", read_only=True
    )
    wish_item_box_name = serializers.CharField(
        source="wish_item_box.name", read_only=True
    )

    class Meta:
        model = WishItem
        fields = [
            "id",
            "wish_item_box_id",
            "wish_item_box_name",
            "product_id",
            "product_name",
            "product_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "wish_item_box_id",
            "wish_item_box_name",
            "created_at",
            "updated_at",
        ]


class WishItemListResponseDTO(serializers.Serializer):
    wish_items = WishItemResponseDTO(many=True)
    total_count = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
