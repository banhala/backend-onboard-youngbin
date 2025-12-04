from rest_framework.routers import DefaultRouter

from member.presentation.member_viewset import MemberViewSet

app_name = "member"

router = DefaultRouter()
router.register(r"", MemberViewSet, basename="member")

urlpatterns = router.urls
