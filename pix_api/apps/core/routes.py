from rest_framework_extensions import routers
from apps.core.views import ReceiverViewSet, DeleteReceiversView
from django.urls import path

app_name = "core"
router = routers.ExtendedSimpleRouter()


router.register(r"receivers", ReceiverViewSet, basename="receivers")

urlpatterns = [
    path(
        "delete-receivers/<str:pk_ids>/",
        DeleteReceiversView.as_view(),
        name="delete-receivers",
    ),
]
urlpatterns += router.urls
