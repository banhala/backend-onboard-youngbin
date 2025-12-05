from __future__ import annotations

from pydantic import BaseModel, Field


class LoginResponseDTO(BaseModel):

    message: str = Field(description="응답 메시지", examples=["success"])
    data: LoginDataDTO = Field(description="로그인 데이터")

    model_config = {
        "frozen": True,
    }


class LoginDataDTO(BaseModel):

    token: str = Field(description="JWT Access Token")
    user_id: int = Field(description="사용자 ID")

    model_config = {
        "frozen": True,
    }
