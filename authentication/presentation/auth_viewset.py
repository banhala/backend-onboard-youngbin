import logging

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from pydantic import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.application.dto.request_dto.login_request_dto import LoginRequestDTO
from authentication.application.dto.request_dto.signup_request_dto import (
    SignupRequestDTO,
)
from authentication.application.dto.response_dto.login_response_dto import (
    LoginResponseDTO,
)
from authentication.application.dto.response_dto.signup_response_dto import (
    SignupResponseDTO,
)
from authentication.domain.auth_service import AuthService
from authentication.exception.auth_already_exist_exception import (
    AuthAlreadyExistException,
)
from authentication.exception.auth_authentication_exception import (
    AuthAuthenticationException,
)
from authentication.exception.auth_invalid_email_exception import (
    AuthInvalidEmailException,
)
from authentication.exception.auth_invalid_password_exception import (
    AuthInvalidPasswordException,
)
from authentication.infrastructure.redis_token_storage import RedisTokenStorage
from common.swagger_utils import pydantic_to_openapi_schema
from member.domain.member_repository import MemberRepository

logger = logging.getLogger(__name__)


class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        repository = MemberRepository()
        self.auth_service = AuthService(repository)

    @swagger_auto_schema(
        operation_summary="회원가입 API",
        operation_description="사용자 회원가입을 처리합니다.",
        request_body=pydantic_to_openapi_schema(SignupRequestDTO),
        responses={
            201: pydantic_to_openapi_schema(SignupResponseDTO),
            400: "Bad Request",
        },
    )
    @action(detail=False, methods=["post"], url_path="signup")
    def signup(self, request):
        try:
            dto = SignupRequestDTO(**request.data)
            self.auth_service.register(str(dto.email), dto.username, dto.password)

            return Response(
                {"message": "회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            logger.warning(f"회원가입 실패 - DTO 검증 오류: {str(e)}")
            errors = e.errors()
            if errors:
                first_error = errors[0]
                field = first_error.get("loc", [""])[0]
                msg = first_error.get("msg", "입력값이 올바르지 않습니다.")
                return Response(
                    {"error": f"{field}: {msg}"}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"error": "입력값이 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (
            AuthInvalidEmailException,
            AuthInvalidPasswordException,
            AuthAlreadyExistException,
        ) as e:
            logger.warning(f"회원가입 실패 - 유효성 검증 오류: {str(e.detail)}")
            return Response(e.detail, status=e.status_code)
        except ValueError as e:
            logger.warning(f"회원가입 실패 - 유효성 검증 오류: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(
                f"회원가입 실패 - email: {request.data.get('email')}, error: {str(e)}"
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="로그인 API",
        operation_description="사용자 로그인을 처리합니다.",
        request_body=pydantic_to_openapi_schema(LoginRequestDTO),
        responses={
            200: pydantic_to_openapi_schema(LoginResponseDTO),
            401: "Unauthorized",
        },
    )
    @action(detail=False, methods=["post"], url_path="signin")
    def signin(self, request):
        try:
            dto = LoginRequestDTO(**request.data)
            member = self.auth_service.login(str(dto.email), dto.password)

            refresh = RefreshToken.for_user(member)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Redis에 토큰 저장
            access_lifetime = int(
                settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
            )
            refresh_lifetime = int(
                settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
            )

            RedisTokenStorage.save_token(member.id, access_token, access_lifetime)
            RedisTokenStorage.save_token(member.id, refresh_token, refresh_lifetime)

            return Response(
                {
                    "message": "success",
                    "data": {
                        "token": access_token,
                        "user_id": member.id,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.warning(f"로그인 실패 - DTO 검증 오류: {str(e)}")
            errors = e.errors()
            if errors:
                first_error = errors[0]
                field = first_error.get("loc", [""])[0]
                msg = first_error.get("msg", "입력값이 올바르지 않습니다.")
                return Response(
                    {"detail": f"{field}: {msg}"}, status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(
                {"detail": "입력값이 올바르지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except (AuthInvalidEmailException, AuthAuthenticationException) as e:
            logger.warning(
                f"로그인 실패 - 인증 오류: {e.detail.get('message', str(e))}"
            )
            return Response(e.detail, status=e.status_code)
        except ValueError as e:
            logger.warning(f"로그인 실패 - 유효성 검증 오류: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.warning(
                f"로그인 실패 - email: {request.data.get('email')}, error: {str(e)}"
            )
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
