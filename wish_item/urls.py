from rest_framework.routers import DefaultRouter

from wish_item.presentation.wish_item_viewset import WishItemViewSet

app_name = "wish_item"

router = DefaultRouter()
router.register(r"", WishItemViewSet, basename="wish_item")

urlpatterns = router.urls
