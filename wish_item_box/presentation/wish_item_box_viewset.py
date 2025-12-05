import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wish_item_box.application.dto.request_dto.wish_item_box_create_request_dto import (
    WishItemBoxCreateRequestDTO,
)
from wish_item_box.application.dto.response_dto.wish_item_box_response_dto import (
    WishItemBoxListResponseDTO,
    WishItemBoxResponseDTO,
)
from wish_item_box.domain.wish_item_box_repository import WishItemBoxRepository
from wish_item_box.domain.wish_item_box_service import WishItemBoxService

logger = logging.getLogger(__name__)


class WishItemBoxViewSet(GenericViewSet):

    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        wish_item_box_repository = WishItemBoxRepository()
        self.wish_item_box_service = WishItemBoxService(wish_item_box_repository)

    @swagger_auto_schema(
        operation_summary="찜 서랍 생성",
        operation_description="새로운 찜 서랍을 생성합니다. 사용자별 찜 서랍 이름은 중복될 수 없습니다.",
        request_body=WishItemBoxCreateRequestDTO,
        responses={
            201: WishItemBoxResponseDTO,
            400: "Bad Request - 중복된 이름",
            401: "Unauthorized",
        },
    )
    def create(self, request):
        try:
            serializer = WishItemBoxCreateRequestDTO(data=request.data)
            serializer.is_valid(raise_exception=True)

            wish_item_box = self.wish_item_box_service.create_wish_item_box(
                member_id=request.user.id, name=serializer.validated_data["name"]
            )

            response_serializer = WishItemBoxResponseDTO(wish_item_box)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(
                f"찜 서랍 생성 실패 - member_id: {request.user.id}, error: {str(e)}"
            )
            raise

    @swagger_auto_schema(
        operation_summary="찜 서랍 삭제",
        operation_description="찜 서랍을 삭제합니다. 서랍에 포함된 찜 상품도 일괄 삭제됩니다 (Cascade).",
        responses={
            204: "No Content",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def destroy(self, request, pk=None):
        try:
            self.wish_item_box_service.delete_wish_item_box(
                member_id=request.user.id, wish_item_box_id=int(pk)
            )

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(
                f"찜 서랍 삭제 실패 - member_id: {request.user.id}, "
                f"wish_item_box_id: {pk}, error: {str(e)}"
            )
            raise

    @swagger_auto_schema(
        operation_summary="찜 서랍 목록 조회",
        operation_description="사용자의 찜 서랍 목록을 페이지네이션하여 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="페이지 번호",
                type=openapi.TYPE_INTEGER,
                default=1,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="페이지 크기",
                type=openapi.TYPE_INTEGER,
                default=20,
            ),
        ],
        responses={
            200: WishItemBoxListResponseDTO,
            401: "Unauthorized",
        },
    )
    def list(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("page_size", 20))

            wish_item_boxes, total_count = (
                self.wish_item_box_service.get_wish_item_boxes(
                    member_id=request.user.id, page=page, page_size=page_size
                )
            )

            response_data = {
                "wish_item_boxes": wish_item_boxes,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
            }

            serializer = WishItemBoxListResponseDTO(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                f"찜 서랍 목록 조회 실패 - member_id: {request.user.id}, error: {str(e)}"
            )
            raise
