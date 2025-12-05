from rest_framework import serializers


class SignupRequestDTO(serializers.Serializer):

    username = serializers.CharField(
        min_length=2,
        max_length=30,
        help_text="사용자명",
    )
    email = serializers.EmailField(help_text="이메일")
    password = serializers.CharField(
        min_length=12,
        help_text="비밀번호",
    )
