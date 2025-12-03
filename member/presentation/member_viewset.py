import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.swagger_utils import pydantic_to_openapi_schema
from member.application.dto.response_dto.member_response_dto import MemberResponseDTO
from member.domain.member_repository import MemberRepository
from member.domain.member_service import MemberService

logger = logging.getLogger(__name__)


class MemberViewSet(GenericViewSet):

    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        repository = MemberRepository()
        self.member_service = MemberService(repository)

    @swagger_auto_schema(
        operation_summary="내 정보 조회",
        operation_description="인증된 사용자 정보 조회 (JWT 토큰 필요)",
        responses={
            200: pydantic_to_openapi_schema(MemberResponseDTO),
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        try:
            if not request.user.is_authenticated:
                return Response(
                    {"error": "Authentication required"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            member = self.member_service.get_member_by_id(request.user.id)

            return Response(
                {
                    "id": member.id,
                    "email": member.email,
                    "username": member.username,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(
                f"회원 정보 조회 실패 - member_id: {request.user.id}, error: {str(e)}"
            )
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
