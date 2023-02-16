from django.db import models
import uuid
from apps.core.choices import (
    pix_key_type_choices,
    receiver_status_choices,
    document_type_choices,
)


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bank(UUIDModel, TimeStampModel):
    name = models.CharField(max_length=100)
    bacen_code = models.CharField(max_length=6, unique=True)
    image_url = models.URLField(max_length=400)

    def __str__(self):
        return f"Bank {self.name} - {self.bacen_code}"


class BankAccount(UUIDModel, TimeStampModel):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    agency = models.CharField(max_length=10)
    agency_digit = models.CharField(max_length=1, default="0")
    account = models.CharField(max_length=10)
    account_digit = models.CharField(max_length=1, default="X")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Bank Account {self.bank.name} - {self.agency} - {self.account}"

    class Meta:
        unique_together = ("bank", "agency", "account")


class Receiver(UUIDModel, TimeStampModel):
    name = models.CharField(max_length=200)
    pix_key = models.CharField(max_length=140)
    pix_key_type = models.CharField(
        max_length=20,
        choices=pix_key_type_choices.to_django_choices(),
        default=pix_key_type_choices.email,
    )
    email = models.EmailField(max_length=250, blank=True, null=True)
    document = models.CharField(max_length=18)
    document_type = models.CharField(
        max_length=4,
        choices=document_type_choices.to_django_choices(),
        default=document_type_choices.cpf,
    )
    status = models.CharField(
        max_length=15,
        choices=receiver_status_choices.to_django_choices(),
        default=receiver_status_choices.rascunho,
    )
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Receiver {self.name} - {self.pix_key_type}"

    class Meta:
        unique_together = ("document", "pix_key", "pix_key_type")
