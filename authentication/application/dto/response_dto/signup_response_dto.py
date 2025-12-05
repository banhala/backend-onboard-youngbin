from __future__ import annotations

from pydantic import BaseModel, Field


class SignupResponseDTO(BaseModel):

    message: str = Field(description="응답 메시지")

    model_config = {
        "frozen": True,
    }
