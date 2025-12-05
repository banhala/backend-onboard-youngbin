from __future__ import annotations

from pydantic import BaseModel, Field


class SignupRequestDTO(BaseModel):

    username: str = Field(
        description="사용자명",
        examples=["youngbin"],
    )
    email: str = Field(description="이메일", examples=["example@a-bly.com"])
    password: str = Field(
        description="비밀번호",
        examples=["Password1234!"],
    )

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
    }
