from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Backend Onboard porject by youngbin",
        default_version="v1",
        description="Backend Onboard porject by youngbin",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("auth/", include("authentication.urls")),
    path("members/", include("member.urls")),
    path("wish-item-boxes/", include("wish_item_box.urls")),
    path("wish-items/", include("wish_item.urls")),
]

handler500 = "common.views.server_error"
