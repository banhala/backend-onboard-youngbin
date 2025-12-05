from rest_framework import serializers


class WishItemCreateRequestDTO(serializers.Serializer):
    wish_item_box_id = serializers.IntegerField(required=True, help_text="찜 서랍 ID")
    product_id = serializers.IntegerField(required=True, help_text="상품 ID")
