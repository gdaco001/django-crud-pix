import pytest
from apps.core.factories import BankAccountFactory
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient(headers={"content_type": "application/json"})
    return client


@pytest.fixture
def create_default_bank_account():
    return BankAccountFactory.create(agency="0000", account="0000000")


@pytest.fixture
def receiver_attributes():
    return {
        "name": "Teste",
        "document": "12345678901",
        "pix_key_type": "EMAIL",
        "pix_key": "teste@teste.com",
        "email": "notification@teste.com",
    }


@pytest.fixture
def expected_attributes_response():
    return {
        "name": "Teste",
        "document": "123.456.789-01",
        "pix_key_type": "EMAIL",
        "pix_key": "TESTE@teste.com",
        "email": "NOTIFICATION@TESTE.COM",
        "status": "RASCUNHO",
    }


@pytest.fixture
def invalid_pix_keys():
    return {
        "CPF": "12345678901",
        "CNPJ": "12345678901234",
        "EMAIL": "teste",
        "TELEFONE": "5511999999999",
        "CHAVE_ALEATORIA": "12345678901234567890123456789012",
    }


@pytest.fixture
def valid_pix_keys():
    return {
        "CPF": "123.456.789-01",
        "CNPJ": "12.345.678/9012-34",
        "EMAIL": "TeStE@teste.com",
        "TELEFONE": "+5511987654321",
        "CHAVE_ALEATORIA": "959b69c0-dc57-4a05-b4e4-22c4ea0f97f0",
    }


def valid_pix_keys_to_internal_value():
    return {
        "CPF": "12345678901",
        "CNPJ": "12345678901234",
        "EMAIL": "teste@teste.com",
        "TELEFONE": "5511987654321",
        "CHAVE_ALEATORIA": "959b69c0-dc57-4a05-b4e4-22c4ea0f97f0",
    }
