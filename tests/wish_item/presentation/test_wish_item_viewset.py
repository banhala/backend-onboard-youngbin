import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from member.model.member import Member
from product.model.product import Product
from wish_item.model.wish_item import WishItem
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


@pytest.fixture
def test_wish_item_box(test_member):
    return WishItemBox.objects.create(member=test_member, name="테스트 서랍")


@pytest.fixture
def test_product():
    return Product.objects.create(
        name="테스트 상품",
        thumbnail="https://image.com/product/thumbnail/example.jpg",
        price=10000,
    )


@pytest.mark.django_db
class TestWishItemViewSet:
    def test_create_wish_item_success(
        self, authenticated_client, test_member, test_wish_item_box, test_product
    ):
        # Given
        url = "/wish-items/"
        data = {
            "wish_item_box_id": test_wish_item_box.id,
            "product_id": test_product.id,
        }

        # When
        response = authenticated_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["product_id"] == test_product.id
        assert response.data["product_name"] == test_product.name
        assert response.data["product_price"] == test_product.price
        assert WishItem.objects.filter(
            wish_item_box=test_wish_item_box, product_id=test_product.id
        ).exists()

    def test_create_wish_item_without_wish_item_box(
        self, authenticated_client, test_member, test_product
    ):
        # Given - 찜 서랍이 없는 상태
        url = "/wish-items/"
        data = {"wish_item_box_id": 1, "product_id": test_product.id}

        # When
        response = authenticated_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_wish_item_duplicate(
        self, authenticated_client, test_member, test_wish_item_box, test_product
    ):
        # Given
        WishItem.objects.create(
            wish_item_box=test_wish_item_box,
            product_id=test_product.id,
            product_name=test_product.name,
            product_price=test_product.price,
        )
        url = "/wish-items/"
        data = {
            "wish_item_box_id": test_wish_item_box.id,
            "product_id": test_product.id,
        }

        # When
        response = authenticated_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_wish_item_product_not_found(
        self, authenticated_client, test_member, test_wish_item_box
    ):
        # Given
        url = "/wish-items/"
        data = {"wish_item_box_id": test_wish_item_box.id, "product_id": 99999}

        # When
        response = authenticated_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_wish_items_success(
        self, authenticated_client, test_member, test_wish_item_box, test_product
    ):
        # Given
        WishItem.objects.create(
            wish_item_box=test_wish_item_box,
            product_id=test_product.id,
            product_name=test_product.name,
            product_price=test_product.price,
        )
        url = f"/wish-items/?wish_item_box_id={test_wish_item_box.id}"

        # When
        response = authenticated_client.get(url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_count"] == 1
        assert len(response.data["wish_items"]) == 1

    def test_list_wish_items_missing_wish_item_box_id(self, authenticated_client):
        # Given
        url = "/wish-items/?page=1&page_size=10"

        # When
        response = authenticated_client.get(url)

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_wish_item_success(
        self, authenticated_client, test_member, test_wish_item_box, test_product
    ):
        # Given
        wish_item = WishItem.objects.create(
            wish_item_box=test_wish_item_box,
            product_id=test_product.id,
            product_name=test_product.name,
            product_price=test_product.price,
        )
        url = f"/wish-items/{wish_item.id}/"

        # When
        response = authenticated_client.delete(url)

        # Then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not WishItem.objects.filter(id=wish_item.id).exists()

    def test_delete_wish_item_not_found(self, authenticated_client):
        # Given
        url = "/wish-items/99999/"

        # When
        response = authenticated_client.delete(url)

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_wish_item_unauthorized(self, api_client, test_product):
        # Given
        url = "/wish-items/"
        data = {"wish_item_box_id": 1, "product_id": test_product.id}

        # When
        response = api_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
