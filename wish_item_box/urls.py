from rest_framework.routers import DefaultRouter

from wish_item_box.presentation.wish_item_box_viewset import WishItemBoxViewSet

app_name = "wish_item_box"

router = DefaultRouter()
router.register(r"", WishItemBoxViewSet, basename="wish_item_box")

urlpatterns = router.urls
