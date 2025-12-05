import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from product.domain.product_repository import ProductRepository
from wish_item.application.dto.request_dto.wish_item_create_request_dto import (
    WishItemCreateRequestDTO,
)
from wish_item.application.dto.response_dto.wish_item_response_dto import (
    WishItemListResponseDTO,
    WishItemResponseDTO,
)
from wish_item.domain.wish_item_repository import WishItemRepository
from wish_item.domain.wish_item_service import WishItemService
from wish_item_box.domain.wish_item_box_repository import WishItemBoxRepository

logger = logging.getLogger(__name__)


class WishItemViewSet(GenericViewSet):

    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        wish_item_repository = WishItemRepository()
        wish_item_box_repository = WishItemBoxRepository()
        product_repository = ProductRepository()
        self.wish_item_service = WishItemService(
            wish_item_repository, wish_item_box_repository, product_repository
        )

    @swagger_auto_schema(
        operation_summary="상품 찜하기",
        operation_description=(
            "특정 찜 서랍에 상품을 추가합니다. "
            "최소 1개의 찜 서랍가 필요하며, 동일 상품은 중복 저장할 수 없습니다."
        ),
        request_body=WishItemCreateRequestDTO,
        responses={
            201: WishItemResponseDTO,
            400: "Bad Request - 중복된 상품 또는 찜 서랍 없음",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def create(self, request):
        try:
            serializer = WishItemCreateRequestDTO(data=request.data)
            serializer.is_valid(raise_exception=True)

            wish_item = self.wish_item_service.add_wish_item(
                member_id=request.user.id,
                wish_item_box_id=serializer.validated_data["wish_item_box_id"],
                product_id=serializer.validated_data["product_id"],
            )

            response_serializer = WishItemResponseDTO(wish_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(
                f"상품 찜하기 실패 - member_id: {request.user.id}, error: {str(e)}"
            )
            raise

    @swagger_auto_schema(
        operation_summary="찜 해제",
        operation_description="찜 서랍에서 상품을 삭제합니다.",
        responses={
            204: "No Content",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def destroy(self, request, pk=None):
        try:
            self.wish_item_service.remove_wish_item(
                member_id=request.user.id, wish_item_id=int(pk)
            )

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(
                f"찜 해제 실패 - member_id: {request.user.id}, "
                f"wish_item_id: {pk}, error: {str(e)}"
            )
            raise

    @swagger_auto_schema(
        operation_summary="찜 목록 조회",
        operation_description="특정 찜 서랍의 상품 목록을 페이지네이션하여 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                "wish_item_box_id",
                openapi.IN_QUERY,
                description="찜 서랍 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
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
            200: WishItemListResponseDTO,
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def list(self, request):
        try:
            wish_item_box_id = request.query_params.get("wish_item_box_id")
            if not wish_item_box_id:
                return Response(
                    {"error": "wish_item_box_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            wish_item_box_id = int(wish_item_box_id)
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("page_size", 20))

            wish_items, total_count = self.wish_item_service.get_wish_items(
                member_id=request.user.id,
                wish_item_box_id=wish_item_box_id,
                page=page,
                page_size=page_size,
            )

            response_data = {
                "wish_items": wish_items,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
            }

            serializer = WishItemListResponseDTO(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                f"찜 목록 조회 실패 - member_id: {request.user.id}, error: {str(e)}"
            )
            raise
