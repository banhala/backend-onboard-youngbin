from __future__ import annotations

from django.http import JsonResponse
from rest_framework import status


def server_error(request, *args, **kwargs):
    return JsonResponse(
        data={"message": "Server Error", "code": "SERVER_ERROR"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
