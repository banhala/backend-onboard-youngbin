from __future__ import annotations

from django.http import UnreadablePostError
from pydantic import ValidationError as PydanticValidationError
from rest_framework.views import exception_handler as drf_exception_handler

from common.exception.invalid_request_exception import InvalidRequestException


def custom_exception_handler(exc, context):

    if isinstance(exc, UnreadablePostError):
        exc = InvalidRequestException("연결이 끊어졌습니다.")

    # Pydantic ValidationError 처리
    if isinstance(exc, PydanticValidationError):
        exc = InvalidRequestException(
            f"잘못된 요청입니다. 올바르게 입력했는지 확인해 주세요. [{str(exc)}]"
        )

    # DRF 기본 예외 핸들러 호출
    response = drf_exception_handler(exc, context)

    return response
