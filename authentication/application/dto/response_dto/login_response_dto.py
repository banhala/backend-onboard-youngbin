from rest_framework import serializers


class LoginDataDTO(serializers.Serializer):
    """로그인 데이터 DTO"""

    token = serializers.CharField(help_text="JWT Access Token")
    user_id = serializers.IntegerField(help_text="사용자 ID")


class LoginResponseDTO(serializers.Serializer):
    """로그인 응답 DTO"""

    message = serializers.CharField(help_text="응답 메시지")
    data = LoginDataDTO(help_text="로그인 데이터")
