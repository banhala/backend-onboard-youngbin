from rest_framework import serializers

from member.model.member import Member


class MemberResponseDTO(serializers.ModelSerializer):
    """회원 응답 DTO"""

    class Meta:
        model = Member
        fields = ["id", "email", "username"]
        read_only_fields = ["id"]
