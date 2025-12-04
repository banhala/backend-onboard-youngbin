from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class MemberResponseDTO(BaseModel):

    id: int = Field(description="회원 ID")
    email: EmailStr = Field(description="이메일")
    username: str = Field(description="사용자명")

    model_config = {
        "frozen": True,
    }
