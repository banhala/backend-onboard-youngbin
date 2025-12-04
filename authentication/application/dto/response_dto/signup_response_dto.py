from rest_framework import serializers


class SignupResponseDTO(serializers.Serializer):
    """회원가입 응답 DTO"""

    message = serializers.CharField(help_text="응답 메시지")
