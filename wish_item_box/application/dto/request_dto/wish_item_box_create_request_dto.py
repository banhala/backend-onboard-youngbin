from rest_framework import serializers


class WishItemBoxCreateRequestDTO(serializers.Serializer):
    name = serializers.CharField(
        max_length=100, required=True, help_text="찜 서랍 이름"
    )

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("찜 서랍 이름은 필수입니다.")
        return value.strip()
