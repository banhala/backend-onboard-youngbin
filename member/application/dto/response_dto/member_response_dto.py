from rest_framework import serializers

from member.model.member import Member


class MemberResponseDTO(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ["id", "email", "username"]
        read_only_fields = ["id"]
