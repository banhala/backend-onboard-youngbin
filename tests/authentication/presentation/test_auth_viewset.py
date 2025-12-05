import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from member.model.member import Member


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user_data():
    return {
        "email": "youngbin2.seo@a-bly.com",
        "username": "youngbin",
        "password": "Password1234!",
    }


@pytest.mark.django_db
class TestAuthViewSetSignup:

    def test_signup_success(self, api_client, test_user_data):
        # Given
        url = reverse("auth:auth-signup")

        # When
        response = api_client.post(url, test_user_data, format="json")

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "회원가입이 완료되었습니다."
        assert Member.objects.filter(email=test_user_data["email"]).exists()

    def test_signup_duplicate_email(self, api_client, test_user_data):
        # Given
        url = reverse("auth:auth-signup")
        api_client.post(url, test_user_data, format="json")

        # When
        response = api_client.post(url, test_user_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "이미 존재하는 이메일" in response.data["message"]
        assert response.data["code"] == "AUTH_ALREADY_EXISTS"

    def test_signup_invalid_email(self, api_client, test_user_data):
        # Given
        url = reverse("auth:auth-signup")
        test_user_data["email"] = "invalid-email"

        # When
        response = api_client.post(url, test_user_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "유효하지 않은 이메일 형식입니다."
        assert response.data["code"] == "AUTH_INVALID_EMAIL"

    def test_signup_password_too_short(self, api_client, test_user_data):
        # Given
        url = reverse("auth:auth-signup")
        test_user_data["password"] = "Pass1!"

        # When
        response = api_client.post(url, test_user_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "최소 12자" in response.data["message"]
        assert response.data["code"] == "AUTH_INVALID_PASSWORD"

    def test_signup_password_no_uppercase(self, api_client, test_user_data):
        # Given
        url = reverse("auth:auth-signup")
        test_user_data["password"] = "password1234!"

        # When
        response = api_client.post(url, test_user_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "대문자" in response.data["message"]
        assert response.data["code"] == "AUTH_INVALID_PASSWORD"

    def test_signup_password_no_special_char(self, api_client, test_user_data):
        # Given
        url = reverse("auth:auth-signup")
        test_user_data["password"] = "Password1234"

        # When
        response = api_client.post(url, test_user_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "특수문자" in response.data["message"]
        assert response.data["code"] == "AUTH_INVALID_PASSWORD"

    def test_signup_missing_required_fields(self, api_client):
        # Given
        url = reverse("auth:auth-signup")
        incomplete_data = {"email": "youngbin.seo@a-bly.com"}

        # When
        response = api_client.post(url, incomplete_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAuthViewSetSignin:

    @pytest.fixture
    def registered_user(self, api_client, test_user_data):
        url = reverse("auth:auth-signup")
        api_client.post(url, test_user_data, format="json")
        return test_user_data

    def test_signin_success(self, api_client, registered_user):
        # Given
        url = reverse("auth:auth-signin")
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        # When
        response = api_client.post(url, login_data, format="json")

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "success"
        assert "token" in response.data["data"]
        assert "user_id" in response.data["data"]

    def test_signin_wrong_password(self, api_client, registered_user):
        # Given
        url = reverse("auth:auth-signin")
        login_data = {
            "email": registered_user["email"],
            "password": "WrongPassword123!",
        }

        # When
        response = api_client.post(url, login_data, format="json")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "로그인 실패" in response.data["message"]
        assert response.data["code"] == "AUTH_AUTHENTICATION_FAILED"

    def test_signin_nonexistent_user(self, api_client):
        # Given
        url = reverse("auth:auth-signin")
        login_data = {
            "email": "nonexistent@a-bly.com",
            "password": "Password1234!",
        }

        # When
        response = api_client.post(url, login_data, format="json")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "로그인 실패" in response.data["message"]

    def test_signin_missing_fields(self, api_client):
        # Given
        url = reverse("auth:auth-signin")
        incomplete_data = {"email": "youngbin.seo@a-bly.com"}

        # When
        response = api_client.post(url, incomplete_data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "이메일과 비밀번호를 입력해주세요."
        assert response.data["code"] == "AUTH_INVALID_INPUT"
