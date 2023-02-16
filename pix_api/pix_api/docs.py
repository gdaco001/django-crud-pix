from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

documentation_view = get_schema_view(
    openapi.Info(
        title="Receivers API",
        default_version="v1",
        description="This is the Receivers API documentation page",
        contact=openapi.Contact(email="gdaco001@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
