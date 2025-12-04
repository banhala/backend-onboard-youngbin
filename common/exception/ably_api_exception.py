from rest_framework import status
from rest_framework.exceptions import APIException


class AblyBaseAPIException(APIException):

    default_detail = "서버 오류가 발생했습니다."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, data: object = None) -> None:
        self.detail = {
            "message": (
                self.message if hasattr(self, "message") else self.default_detail
            ),
        }
        if hasattr(self, "code"):
            self.detail["code"] = self.code
        if hasattr(self, "title"):
            self.detail["title"] = self.title
        self._data = data
