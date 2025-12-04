import re

from member.domain.member_repository import MemberRepository
from member.exception.member_already_exist import MemberAlreadyExistException
from member.exception.member_authentication import MemberAuthenticationException
from member.exception.member_invalid_email import MemberInvalidEmailException
from member.exception.member_invalid_password import MemberInvalidPasswordException
from member.exception.member_not_found import MemberNotFoundException

MIN_PASSWORD_LENGTH = 12
EMAIL_PATTERN = r"^[^@]+@[^@]+\.[^@]+$"
UPPERCASE_PATTERN = r"[A-Z]"
LOWERCASE_PATTERN = r"[a-z]"
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*(),.?":{}|<>]'


class MemberService:
    def __init__(self, repository: MemberRepository) -> None:
        self.repository = repository

    def validate_email(self, email: str) -> None:
        if not re.match(EMAIL_PATTERN, email):
            raise MemberInvalidEmailException(
                f"{email}는 유효하지 않은 이메일 패턴입니다. (요구 패턴 : '??@??.??')"
            )

    def validate_password(self, password: str) -> None:
        if len(password) < MIN_PASSWORD_LENGTH:
            raise MemberInvalidPasswordException(
                f"비밀번호는 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다."
            )

        if not re.search(UPPERCASE_PATTERN, password):
            raise MemberInvalidPasswordException("비밀번호는 대문자를 포함해야 합니다.")

        if not re.search(LOWERCASE_PATTERN, password):
            raise MemberInvalidPasswordException("비밀번호는 소문자를 포함해야 합니다.")

        if not re.search(SPECIAL_CHAR_PATTERN, password):
            raise MemberInvalidPasswordException(
                "비밀번호는 특수문자를 포함해야 합니다."
            )

    def register(self, email: str, username: str, password: str):
        if not email or not username or not password:
            raise ValueError("이메일, 유저명, 비밀번호는 필수값입니다.")

        self.validate_email(email)
        self.validate_password(password)

        if self.repository.exists_by_email(email):
            raise MemberAlreadyExistException(email)

        return self.repository.save(email, username, password)

    def login(self, email: str, password: str):
        if not email or not password:
            raise ValueError("이메일, 유저명, 비밀번호는 필수값입니다.")

        member = self.repository.authenticate(email, password)
        if not member:
            raise MemberAuthenticationException(
                "로그인 실패: 이메일 또는 비밀번호가 올바르지 않습니다."
            )

        return member

    def get_member_by_id(self, member_id: int):
        member = self.repository.find_by_id(member_id)
        if not member:
            raise MemberNotFoundException(
                f"회원을 찾을 수 없습니다. member_id: {member_id}"
            )
        return member
