from django_filters import rest_framework as filters
from django_filters import Filter

from apps.core.models import Receiver
from utils.re_patterns import turn_cpf_cnpj_telefone_into_numeric


class ListFilter(Filter):
    """This resource is responsible for filtering a list of values from a query param."""

    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = "in"
        values = value.split(",")
        return super().filter(qs, values)


class ListFilterUnmaskedPixKeys(Filter):
    """This resource is responsible for unmasking the pix_keys for CPF, CNPJ and TELEFONE."""

    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = "in"
        values = value.split(",")
        for i, string_value in enumerate(values):
            values[i] = turn_cpf_cnpj_telefone_into_numeric(string_value)
        return super().filter(qs, values)


class ReceiverFilterSet(filters.FilterSet):
    pix_key = ListFilterUnmaskedPixKeys(
        field_name="pix_key",
        help_text="Filter by pix_key, multiple values may be separated by commas",
    )
    pix_key_type = ListFilter(
        field_name="pix_key_type",
        help_text="Filter by pix_key_type, multiple values may be separated by commas",
    )
    name = ListFilter(
        field_name="name",
        help_text="Filter by name, multiple values may be separated by commas",
    )
    status = ListFilter(
        field_name="status",
        help_text="Filter by status, multiple values may be separated by commas",
    )

    class Meta:
        model = Receiver
        fields = {
            "pix_key": ["exact"],
            "pix_key_type": ["exact"],
            "name": ["exact", "contains"],
            "status": ["exact"],
        }
