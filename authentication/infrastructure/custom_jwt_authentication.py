from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as SimpleJWTAuthentication,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from authentication.infrastructure.redis_token_storage import RedisTokenStorage

User = get_user_model()


class CustomJWTAuthentication(BaseAuthentication):

    def __init__(self) -> None:
        self.jwt_auth = SimpleJWTAuthentication()

    def authenticate(self, request):
        try:
            raw_token = self.jwt_auth.get_raw_token(self.jwt_auth.get_header(request))
            validated_token = self.jwt_auth.get_validated_token(raw_token)

            user_id = validated_token.get("user_id")
            if not user_id:
                raise AuthenticationFailed("토큰에 user_id가 없습니다.")

            token_string = (
                raw_token.decode("utf-8")
                if isinstance(raw_token, bytes)
                else str(raw_token)
            )
            if not RedisTokenStorage.is_valid_token(token_string):
                raise AuthenticationFailed("토큰이 만료되었거나 유효하지 않습니다.")

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed("사용자를 찾을 수 없습니다.")

            return (user, validated_token)

        except (InvalidToken, TokenError) as e:
            # 토큰 만료 여부 확인
            error_str = str(e)
            if "expired" in error_str.lower():
                raise AuthenticationFailed("토큰이 만료되었습니다.")
            else:
                raise AuthenticationFailed("유효하지 않은 토큰입니다.")
        except AuthenticationFailed:
            raise
        except Exception:
            return None

    def authenticate_header(self, request) -> str:
        return 'Bearer realm="api"'
