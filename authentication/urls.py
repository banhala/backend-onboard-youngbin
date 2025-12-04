from rest_framework.routers import DefaultRouter

from authentication.presentation.auth_viewset import AuthViewSet

app_name = "auth"

router = DefaultRouter()
router.register(r"", AuthViewSet, basename="auth")

urlpatterns = router.urls
