import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from member.model.member import Member
from wish_item_box.model.wish_item_box import WishItemBox


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
    from django.conf import settings

    from authentication.infrastructure.redis_token_storage import RedisTokenStorage

    refresh = RefreshToken.for_user(test_member)
    access_token = str(refresh.access_token)

    access_lifetime = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    RedisTokenStorage.save_token(test_member.id, access_token, access_lifetime)

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.mark.django_db
class TestWishItemBoxViewSet:
    def test_create_wish_item_box_success(self, authenticated_client, test_member):
        # Given
        url = "/wish-item-boxes/"
        data = {"name": "내 찜 서랍"}

        # When
        response = authenticated_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "내 찜 서랍"
        assert WishItemBox.objects.filter(
            member=test_member, name="내 찜 서랍"
        ).exists()

    def test_create_wish_item_box_duplicate_name(
        self, authenticated_client, test_member
    ):
        # Given
        WishItemBox.objects.create(member=test_member, name="중복 서랍")
        url = "/wish-item-boxes/"
        data = {"name": "중복 서랍"}

        # When
        response = authenticated_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_wish_item_boxes_success(self, authenticated_client, test_member):
        # Given
        WishItemBox.objects.create(member=test_member, name="서랍1")
        WishItemBox.objects.create(member=test_member, name="서랍2")
        url = "/wish-item-boxes/?page=1&page_size=10"

        # When
        response = authenticated_client.get(url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_count"] == 2
        assert len(response.data["wish_item_boxes"]) == 2

    def test_delete_wish_item_box_success(self, authenticated_client, test_member):
        # Given
        wish_item_box = WishItemBox.objects.create(
            member=test_member, name="삭제할 서랍"
        )
        url = f"/wish-item-boxes/{wish_item_box.id}/"

        # When
        response = authenticated_client.delete(url)

        # Then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not WishItemBox.objects.filter(id=wish_item_box.id).exists()

    def test_delete_wish_item_box_not_found(self, authenticated_client):
        # Given
        url = "/wish-item-boxes/99999/"

        # When
        response = authenticated_client.delete(url)

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_wish_item_box_unauthorized(self, api_client):
        # Given
        url = "/wish-item-boxes/"
        data = {"name": "내 찜 서랍"}

        # When
        response = api_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
