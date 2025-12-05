from rest_framework import serializers


class SignupResponseDTO(serializers.Serializer):

    message = serializers.CharField(help_text="응답 메시지")
