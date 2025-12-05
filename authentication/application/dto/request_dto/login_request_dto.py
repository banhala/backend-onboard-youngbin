from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequestDTO(BaseModel):

    email: str = Field(description="이메일", examples=["example@a-bly.com"])
    password: str = Field(description="비밀번호", examples=["Password1234!"])

    model_config = {
        "frozen": True,
        "str_strip_whitespace": True,
    }
