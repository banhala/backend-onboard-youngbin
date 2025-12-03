import re

from authentication.exception.auth_already_exist_exception import (
    AuthAlreadyExistException,
)
from authentication.exception.auth_authentication_exception import (
    AuthAuthenticationException,
)
from authentication.exception.auth_invalid_email_exception import (
    AuthInvalidEmailException,
)
from authentication.exception.auth_invalid_password_exception import (
    AuthInvalidPasswordException,
)
from member.domain.member_repository import MemberRepository

MIN_PASSWORD_LENGTH = 12
EMAIL_PATTERN = r"^[^@]+@[^@]+\.[^@]+$"
UPPERCASE_PATTERN = r"[A-Z]"
LOWERCASE_PATTERN = r"[a-z]"
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*(),.?":{}|<>]'


class AuthService:
    def __init__(self, repository: MemberRepository) -> None:
        self.repository = repository

    def validate_email(self, email: str) -> None:
        if not re.match(EMAIL_PATTERN, email):
            raise AuthInvalidEmailException(
                f"{email}는 유효하지 않은 이메일 패턴입니다. (요구 패턴 : '??@??.??')"
            )

    def validate_password(self, password: str) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise AuthInvalidPasswordException(
                f"비밀번호는 최소 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다."
            )

        if not re.search(UPPERCASE_PATTERN, password):
            raise AuthInvalidPasswordException("비밀번호는 대문자를 포함해야 합니다.")

        if not re.search(LOWERCASE_PATTERN, password):
            raise AuthInvalidPasswordException("비밀번호는 소문자를 포함해야 합니다.")

        if not re.search(SPECIAL_CHAR_PATTERN, password):
            raise AuthInvalidPasswordException("비밀번호는 특수문자를 포함해야 합니다.")

    def register(self, email: str, username: str, password: str):
        if not email or not username or not password:
            raise ValueError("이메일, 유저명, 비밀번호는 필수값입니다.")

        self.validate_email(email)
        self.validate_password(password)

        if self.repository.exists_by_email(email):
            raise AuthAlreadyExistException(email)

        return self.repository.save(email, username, password)

    def login(self, email: str, password: str):
        if not email or not password:
            raise ValueError("이메일, 유저명, 비밀번호는 필수값입니다.")

        member = self.repository.authenticate(email, password)
        if not member:
            raise AuthAuthenticationException(
                "로그인 실패: 이메일 또는 비밀번호가 올바르지 않습니다."
            )

        return member
