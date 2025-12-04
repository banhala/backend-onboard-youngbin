from rest_framework import serializers


class LoginRequestDTO(serializers.Serializer):
    """로그인 요청 DTO"""

    email = serializers.CharField(help_text="이메일")
    password = serializers.CharField(help_text="비밀번호")
