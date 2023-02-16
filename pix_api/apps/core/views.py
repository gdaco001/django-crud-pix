from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from apps.core.models import Receiver

from apps.core.serializers import (
    ReceiverSerializer,
    ReceiverCreateUpdateSerializer,
)
from apps.core.filters import ReceiverFilterSet
from apps.core.mixins import MultiSerializerViewSetMixin
from rest_framework import status
from rest_framework.response import Response


class ReceiverViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """This resource is used to handle receivers."""

    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer
    serializer_action_classes = {
        "create": ReceiverCreateUpdateSerializer,
        "update": ReceiverCreateUpdateSerializer,
        "partial_update": ReceiverCreateUpdateSerializer,
    }
    filterset_class = ReceiverFilterSet
    ordering_fields = "created_at"
    ordering = "-created_at"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DeleteReceiversView(APIView):
    """This resource is responsible to bulk delete receivers."""

    def delete(self, request, pk_ids):
        ids = [pk for pk in pk_ids.split(",")]
        for i in ids:
            get_object_or_404(Receiver, pk=i).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
