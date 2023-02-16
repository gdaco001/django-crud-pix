from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from .docs import documentation_view

urlpatterns = [
    re_path(r"^v1/docs/", documentation_view.with_ui("swagger"), name="documentation"),
    path("admin/", admin.site.urls),
    path("v1/", include("apps.core.routes")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
