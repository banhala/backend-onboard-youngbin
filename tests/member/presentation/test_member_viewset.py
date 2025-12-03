import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from member.model.member import Member


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_member():
    member = Member.objects.create_user(
        email="youngbin.seo@a-bly.com",
        username="youngbin",
        password="Password1234!",
    )
    return member


@pytest.fixture
def authenticated_client(api_client, test_member):
    # 로그인하여 토큰 발급
    from django.conf import settings
    from rest_framework_simplejwt.tokens import RefreshToken

    from authentication.infrastructure.redis_token_storage import RedisTokenStorage

    refresh = RefreshToken.for_user(test_member)
    access_token = str(refresh.access_token)

    # Redis에 토큰 저장
    access_lifetime = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    RedisTokenStorage.save_token(test_member.id, access_token, access_lifetime)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.mark.django_db
class TestMemberViewSet:
    def test_get_my_info_success(self, authenticated_client, test_member):

        # Given
        url = reverse("member:member-me")

        # When
        response = authenticated_client.get(url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == test_member.email
        assert response.data["username"] == test_member.username

    def test_get_my_info_unauthorized(self, api_client):
        # Given
        url = reverse("member:member-me")

        # When
        response = api_client.get(url)

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
