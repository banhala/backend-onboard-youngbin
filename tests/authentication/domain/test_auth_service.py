import pytest

from authentication.domain.auth_service import AuthService
from authentication.exception.auth_already_exist_exception import (
    AuthAlreadyExistException,
)
from authentication.exception.auth_invalid_email_exception import (
    AuthInvalidEmailException,
)
from authentication.exception.auth_invalid_password_exception import (
    AuthInvalidPasswordException,
)
from member.domain.member_repository import MemberRepository


@pytest.fixture
def auth_service():
    repository = MemberRepository()
    return AuthService(repository)


class TestAuthService:

    def test_validate_email_success(self, auth_service):
        # Given
        valid_email = "youngbin.seo@a-bly.com"

        # When & Then
        auth_service.validate_email(valid_email)

    def test_validate_email_invalid_pattern(self, auth_service):
        # Given
        invalid_emails = [
            "youngbin",
            "youngbin@",
            "@a-bly.com",
            "youngbin.a-bly.com",
        ]

        # When & Then
        for email in invalid_emails:
            with pytest.raises(AuthInvalidEmailException) as exc_info:
                auth_service.validate_email(email)
            assert "이메일 패턴" in str(exc_info.value.detail["message"])

    def test_validate_password_success(self, auth_service):
        # Given
        valid_password = "Password1234!"

        # When & Then
        auth_service.validate_password(valid_password)

    def test_validate_password_too_short(self, auth_service):
        # Given
        short_password = "Pass1!"

        # When & Then
        with pytest.raises(AuthInvalidPasswordException) as exc_info:
            auth_service.validate_password(short_password)
        assert "최소 12자 이상" in str(exc_info.value.detail["message"])

    def test_validate_password_no_uppercase(self, auth_service):
        # Given
        password = "password1234!"

        # When & Then
        with pytest.raises(AuthInvalidPasswordException) as exc_info:
            auth_service.validate_password(password)
        assert "대문자" in str(exc_info.value.detail["message"])

    def test_validate_password_no_lowercase(self, auth_service):
        # Given
        password = "PASSWORD123!"

        # When & Then
        with pytest.raises(AuthInvalidPasswordException) as exc_info:
            auth_service.validate_password(password)
        assert "소문자" in str(exc_info.value.detail["message"])

    def test_validate_password_no_special_char(self, auth_service):
        # Given
        password = "Password1234"

        # When & Then
        with pytest.raises(AuthInvalidPasswordException) as exc_info:
            auth_service.validate_password(password)
        assert "특수문자" in str(exc_info.value.detail["message"])

    @pytest.mark.django_db
    def test_register_success(self, auth_service):
        # Given
        email = "youngbin.seo@a-bly.com"
        username = "youngbin"
        password = "Password1234!"

        # When
        member = auth_service.register(email, username, password)

        # Then
        assert member is not None
        assert member.email == email
        assert member.username == username

    @pytest.mark.django_db
    def test_register_duplicate_email(self, auth_service):
        # Given
        email = "youngbin.seo@a-bly.com"
        username = "youngbin"
        password = "Password12345!"

        auth_service.register(email, username, password)

        # When & Then
        with pytest.raises(AuthAlreadyExistException) as exc_info:
            auth_service.register(email, "user2", password)
        assert "이미 존재하는 이메일" in str(exc_info.value.detail["message"])

    @pytest.mark.django_db
    def test_register_invalid_email(self, auth_service):
        # Given
        invalid_email = "invalid-email"
        username = "youngbin"
        password = "Password123!"

        # When & Then
        with pytest.raises(AuthInvalidEmailException):
            auth_service.register(invalid_email, username, password)

    @pytest.mark.django_db
    def test_register_invalid_password(self, auth_service):
        # Given
        email = "youngbin2.seo@a-bly.com"
        username = "user"
        invalid_password = "weak"

        # When & Then
        with pytest.raises(AuthInvalidPasswordException):
            auth_service.register(email, username, invalid_password)
