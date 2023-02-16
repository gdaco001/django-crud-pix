import pytest
from apps.core.choices import (
    document_type_choices,
    pix_key_type_choices,
    receiver_status_choices,
)
from apps.core.models import Bank, BankAccount, Receiver
from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db


class TestModels:
    def test_bank_str_dunder_method(self):
        bank = Bank(
            name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
        )
        assert str(bank) == "Bank Banco do Brasil - 001"

    def test_bank_unique_constraint(self):
        Bank.objects.create(
            name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
        )

        with pytest.raises(IntegrityError):
            Bank.objects.create(
                name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
            )

    def test_bank_account_str_dunder_method(self):
        bank = Bank.objects.create(
            name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
        )
        bank_account = BankAccount.objects.create(
            bank=bank, agency="1234", account="5678"
        )
        assert str(bank_account) == "Bank Account Banco do Brasil - 1234 - 5678"

    def test_bank_account_unique_together(self):
        bank = Bank.objects.create(
            name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
        )
        BankAccount.objects.create(bank=bank, agency="1234", account="5678")

        with pytest.raises(IntegrityError):
            BankAccount.objects.create(bank=bank, agency="1234", account="5678")

    def test_receiver_str_dunder_method(self):
        bank = Bank.objects.create(
            name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
        )
        bank_account = BankAccount.objects.create(
            bank=bank, agency="0000", account="0000000"
        )
        receiver = Receiver.objects.create(
            name="Teste Teste",
            pix_key="TESTE@TESTE.COM",
            pix_key_type=pix_key_type_choices.email,
            email="NOTIFICATION@TESTE.COM",
            document="10340182478",
            document_type=document_type_choices.cpf,
            status=receiver_status_choices.validado,
            bank_account=bank_account,
        )
        assert str(receiver) == "Receiver Teste Teste - EMAIL"

    def test_receiver_unique_together(self):
        bank = Bank.objects.create(
            name="Banco do Brasil", bacen_code="001", image_url="http://s3_url.com"
        )
        bank_account = BankAccount.objects.create(
            bank=bank, agency="1234", account="5678"
        )
        Receiver.objects.create(
            name="Teste Teste",
            pix_key="TESTE@TESTE.COM",
            pix_key_type=pix_key_type_choices.email,
            email="NOTIFICATION@TESTE.COM",
            document="10340182478",
            document_type=document_type_choices.cpf,
            status=receiver_status_choices.validado,
            bank_account=bank_account,
        )

        with pytest.raises(IntegrityError):
            Receiver.objects.create(
                name="Teste Teste",
                pix_key="TESTE@TESTE.COM",
                pix_key_type=pix_key_type_choices.email,
                email="NOTIFICATION@TESTE.COM",
                document="10340182478",
                document_type=document_type_choices.cpf,
                status=receiver_status_choices.validado,
                bank_account=bank_account,
            )
