from rest_framework import serializers

from wish_item_box.model.wish_item_box import WishItemBox


class WishItemBoxResponseDTO(serializers.ModelSerializer):

    class Meta:
        model = WishItemBox
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class WishItemBoxListResponseDTO(serializers.Serializer):
    wish_item_boxes = WishItemBoxResponseDTO(many=True)
    total_count = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
