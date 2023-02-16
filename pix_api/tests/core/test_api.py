import re
from copy import deepcopy

import pytest
from apps.core.choices import pix_key_type_choices, receiver_status_choices
from apps.core.factories import ReceiverFactory
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


class TestReceiverViewSet:
    @pytest.mark.parametrize(
        "field_name, random_create_batch_dict, create_dict",
        [
            (
                "status",
                {"status": receiver_status_choices.rascunho},
                {"status": receiver_status_choices.validado},
            ),
            (
                "name",
                {},
                {"name": "Test Name"},
            ),
            (
                "pix_key_type",
                {"pix_key_type": pix_key_type_choices.telefone},
                {"pix_key_type": pix_key_type_choices.cpf},
            ),
            (
                "pix_key",
                {"pix_key_type": pix_key_type_choices.cpf, "pix_key": "123.456.789-01"},
                {
                    "pix_key_type": pix_key_type_choices.cnpj,
                    "pix_key": "12345678901234",
                },
            ),
        ],
    )
    def test_filter_receivers(
        self, client, field_name, random_create_batch_dict, create_dict
    ):
        ReceiverFactory.create_batch(4, **random_create_batch_dict)
        ReceiverFactory.create(**create_dict)

        response = client.get(
            reverse("core:receivers-list"),
            {field_name: create_dict[field_name]},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    @pytest.mark.parametrize(
        "field_name, random_create_batch_dict, create_dict_1, create_dict_2",
        [
            (
                "status",
                {"status": receiver_status_choices.rascunho},
                {"status": receiver_status_choices.validado},
                {"status": receiver_status_choices.invalido},
            ),
            (
                "name",
                {},
                {"name": "Test Name"},
                {"name": "National Bank"},
            ),
            (
                "pix_key_type",
                {"pix_key_type": pix_key_type_choices.telefone},
                {"pix_key_type": pix_key_type_choices.cpf},
                {"pix_key_type": pix_key_type_choices.cnpj},
            ),
            (
                "pix_key",
                {"pix_key_type": pix_key_type_choices.cpf, "pix_key": "123.456.789-01"},
                {
                    "pix_key_type": pix_key_type_choices.cnpj,
                    "pix_key": "12345678901234",
                },
                {
                    "pix_key_type": pix_key_type_choices.cnpj,
                    "pix_key": "21333876219043",
                },
            ),
        ],
    )
    def test_filter_receivers_list(
        self, client, field_name, random_create_batch_dict, create_dict_1, create_dict_2
    ):
        ReceiverFactory.create_batch(4, **random_create_batch_dict)
        ReceiverFactory.create(**create_dict_1)
        ReceiverFactory.create(**create_dict_2)

        response = client.get(
            reverse("core:receivers-list"),
            {field_name: f"{create_dict_1[field_name]},{create_dict_2[field_name]}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_list_receivers_and_pagination(self, client):
        ReceiverFactory.create_batch(30)
        response = client.get(reverse("core:receivers-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 30
        assert len(response.data["results"]) == settings.PAGE_SIZE

    @pytest.mark.parametrize(
        "pix_key_type, pix_key_value",
        [
            (pix_key_type_choices.cpf, "123.456.789-01"),
            (pix_key_type_choices.cpf, "12345678901"),
            (pix_key_type_choices.cnpj, "12.345.678/9012-34"),
            (pix_key_type_choices.cnpj, "12345678901234"),
            (pix_key_type_choices.email, "TeStE@teste.com"),
            (pix_key_type_choices.email, "teste@teste.com"),
            (pix_key_type_choices.telefone, "559298765-4321"),
            (pix_key_type_choices.telefone, "5592987654321"),
            (pix_key_type_choices.chave, "959b69c0-dc57-4a05-b4e4-22c4ea0f97f0"),
        ],
    )
    def test_filter_receivers_pix_key_with_masked_and_unmasked_values(
        self, client, pix_key_type, pix_key_value
    ):
        ReceiverFactory.create_batch(5)
        if pix_key_type in [pix_key_type_choices.cpf, pix_key_type_choices.cnpj]:
            ReceiverFactory.create(
                pix_key_type=pix_key_type, pix_key=re.sub("[^0-9]", "", pix_key_value)
            )
        else:
            ReceiverFactory.create(pix_key_type=pix_key_type, pix_key=pix_key_value)
        response = client.get(
            reverse("core:receivers-list"), {"pix_key": pix_key_value}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    @pytest.mark.parametrize(
        "pix_key_type, pix_key_value",
        [
            (pix_key_type_choices.cpf, "123.456.789-01"),
            (pix_key_type_choices.cpf, "12345678901"),
            (pix_key_type_choices.cnpj, "12.345.678/9012-34"),
            (pix_key_type_choices.cnpj, "12345678901234"),
            (pix_key_type_choices.email, "TeStE@teste.com"),
            (pix_key_type_choices.email, "teste@teste.com"),
            (pix_key_type_choices.telefone, "559298765-4321"),
            (pix_key_type_choices.telefone, "5592987654321"),
            (pix_key_type_choices.chave, "959b69c0-dc57-4a05-b4e4-22c4ea0f97f0"),
        ],
    )
    def test_create_receiver(
        self,
        api_client,
        receiver_attributes,
        pix_key_type,
        pix_key_value,
        expected_attributes_response,
        create_default_bank_account,
    ):
        url = reverse("core:receivers-list")
        receiver_attributes["pix_key_type"] = expected_attributes_response[
            "pix_key_type"
        ] = pix_key_type
        receiver_attributes["pix_key"] = pix_key_value
        expected_attributes_response["pix_key"] = pix_key_value

        if pix_key_type in [
            pix_key_type_choices.cpf,
            pix_key_type_choices.cnpj,
            pix_key_type_choices.telefone,
        ]:
            pix_key_value = re.sub("[^0-9]", "", pix_key_value)
            expected_attributes_response["pix_key"] = pix_key_value

        elif pix_key_type == pix_key_type_choices.email:
            expected_attributes_response["pix_key"] = pix_key_value.upper()

        response = api_client.post(url, data=receiver_attributes)
        assert response.status_code == status.HTTP_201_CREATED
        for key in expected_attributes_response.keys():
            assert expected_attributes_response[key] == response.data[key]

    @pytest.mark.parametrize(
        "pix_key_type, pix_key_value",
        [
            (pix_key_type_choices.cpf, "12f.456.789-01"),
            (pix_key_type_choices.cpf, "1sd78901"),
            (pix_key_type_choices.cnpj, "12.345.67-/901234"),
            (pix_key_type_choices.cnpj, "123fs78901234"),
            (pix_key_type_choices.email, "TeStE@teste/com"),
            (pix_key_type_choices.email, "testeteste.com"),
            (pix_key_type_choices.telefone, "59298765-4321"),
            (pix_key_type_choices.telefone, "559987654321"),
            (pix_key_type_choices.chave, "959b69c0dc57-4a05b4e4-22c4ea0f97f0"),
        ],
    )
    def test_create_with_invalid_pix_keys(
        self,
        api_client,
        receiver_attributes,
        pix_key_type,
        pix_key_value,
        create_default_bank_account,
    ):
        url = reverse("core:receivers-list")
        receiver_attributes["pix_key"] = pix_key_value
        receiver_attributes["pix_key_type"] = pix_key_type
        response = api_client.post(url, data=receiver_attributes)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_with_empty_email(
        self, api_client, receiver_attributes, create_default_bank_account
    ):
        url = reverse("core:receivers-list")
        receiver_attributes["email"] = ""
        response = api_client.post(url, data=receiver_attributes)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_with_invalid_email(
        self, api_client, receiver_attributes, create_default_bank_account
    ):
        url = reverse("core:receivers-list")
        receiver_attributes["email"] = "a.2.@teste@.com"
        response = api_client.post(url, data=receiver_attributes)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_duplicate_document_pix_type_pix_value(
        self, api_client, receiver_attributes, create_default_bank_account
    ):
        url = reverse("core:receivers-list")
        receiver = ReceiverFactory.create(
            document="10340192435",
            pix_key_type=pix_key_type_choices.email,
            pix_key="EMAIL@TESTE.COM",
        )
        receiver_attributes["document"] = receiver.document
        receiver_attributes["pix_key_type"] = receiver.pix_key_type
        receiver_attributes["pix_key"] = receiver.pix_key

        response = api_client.post(url, receiver_attributes)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @pytest.mark.parametrize(
        "receiver_status",
        [receiver_status_choices.rascunho, receiver_status_choices.validado],
    )
    def test_update_receiver(self, api_client, receiver_attributes, receiver_status):
        receiver = ReceiverFactory.create(
            document="10340192435",
            pix_key_type=pix_key_type_choices.email,
            pix_key="EMAIL@TESTE.COM",
            status=receiver_status,
        )

        receiver_attributes["name"] = receiver.name

        response_attributes = deepcopy(receiver_attributes)
        response_attributes["document"] = "103.401.924-35"
        response_attributes["pix_key"] = receiver.pix_key

        receiver_attributes["document"] = "999.401.929-99"
        receiver_attributes["pix_key_type"] = pix_key_type_choices.chave
        receiver_attributes["pix_key"] = "959b69c0-dc57-4a05-b4e4-22c4ea0f97f0"
        receiver_attributes["email"] = response_attributes[
            "email"
        ] = "NOVOEMAIL@TESTE.COM"

        url = reverse("core:receivers-detail", [receiver.id])
        response = api_client.put(url, receiver_attributes)

        receiver_attributes["status"] = receiver_status

        if receiver_status == receiver_status_choices.rascunho:
            for key in receiver_attributes.keys():
                assert receiver_attributes[key] == response.data[key]
        else:
            for key in response_attributes.keys():
                assert response_attributes[key] == response.data[key]

    def test_delete_in_bulk(self, api_client):
        receivers = ReceiverFactory.create_batch(3)
        url = (
            "/v1/delete-receivers/"
            + f"{receivers[0].id},{receivers[1].id},{receivers[2].id}/"
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
