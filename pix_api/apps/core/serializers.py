from rest_framework import serializers
import re
from apps.core.models import Receiver, Bank, BankAccount
from apps.core.choices import (
    receiver_status_choices,
    document_type_choices,
    pix_key_type_choices,
)
from utils.re_patterns import (
    PATTERN_MAP,
    mask_document,
    mask_pix_key,
    unmask_pix_key,
    convert_to_numerals,
)
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from apps.core.factories import ReceiverFactory
from utils.exceptions import ReceiverAlreadyExistsApiException


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("name", "bacen_code", "image_url")


class BankAccountSerializer(serializers.ModelSerializer):
    bank = BankSerializer()

    class Meta:
        model = BankAccount
        fields = (
            "bank",
            "agency",
            "agency_digit",
            "account",
            "account_digit",
            "is_active",
        )


class ReceiverSerializer(serializers.ModelSerializer):
    bank_account = BankAccountSerializer(read_only=True)

    def to_representation(self, data):
        response = {
            "id": data.id,
            "name": data.name,
            "document_type": data.document_type,
            "document": mask_document(data.document),
            "pix_key_type": data.pix_key_type,
            "pix_key": mask_pix_key(data.pix_key, data.pix_key_type),
            "email": data.email,
            "status": data.status,
            "bank_account": BankAccountSerializer(data.bank_account).data,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
        }
        return response

    class Meta:
        model = Receiver
        fields = "__all__"


class ReceiverCreateUpdateSerializer(
    PartialUpdateSerializerMixin, serializers.Serializer
):
    name = serializers.CharField(
        max_length=200, required=True, allow_null=False, allow_blank=False
    )
    document = serializers.CharField(
        max_length=18, required=True, allow_null=False, allow_blank=False
    )
    pix_key = serializers.CharField(
        max_length=140, required=True, allow_null=False, allow_blank=False
    )
    pix_key_type = serializers.ChoiceField(
        choices=pix_key_type_choices.to_django_choices(),
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=receiver_status_choices.to_django_choices(),
        required=False,
        allow_null=True,
    )

    def validate(self, data):
        pix_key_type = data.get("pix_key_type")
        pix_key = data.get("pix_key")

        if not re.match(PATTERN_MAP[pix_key_type], pix_key):
            raise serializers.ValidationError(
                {"pix_key": f"Invalid pix_key for type {pix_key_type}"}
            )

        return data

    def validate_document(self, value):
        if re.match(PATTERN_MAP["CPF"], value) is not None:
            return value
        elif re.match(PATTERN_MAP["CNPJ"], value) is not None:
            return value
        raise serializers.ValidationError("Document is invalid")

    def validate_email(self, value):
        if value and re.match(PATTERN_MAP["EMAIL"], value) is not None:
            return value
        elif not value:
            return value
        raise serializers.ValidationError("Notification e-mail is invalid")

    def to_internal_value(self, data):
        if data.get("email"):
            data["email"] = data["email"].upper()
        if data.get("pix_key_type") == pix_key_type_choices.email:
            if data.get("pix_key"):
                data["pix_key"] = data["pix_key"].upper()
        return super().to_internal_value(data)

    def to_representation(self, data):
        response = {
            "id": data.id,
            "name": data.name,
            "document_type": data.document_type,
            "document": mask_document(data.document),
            "pix_key_type": data.pix_key_type,
            "pix_key": mask_pix_key(data.pix_key, data.pix_key_type),
            "email": data.email,
            "status": data.status,
            "bank_account": BankAccountSerializer(data.bank_account).data,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
        }

        return response

    def create(self, validated_data):
        validated_data["pix_key"] = unmask_pix_key(
            validated_data["pix_key"], validated_data["pix_key_type"]
        )
        validated_data["document"] = convert_to_numerals(validated_data["document"])
        validated_data["bank_account"] = BankAccount.objects.get(
            agency="0000", account="0000000"
        )
        validated_data["document_type"] = (
            document_type_choices.cpf
            if re.match(PATTERN_MAP["CPF"], validated_data["document"]) is not None
            else document_type_choices.cnpj
        )
        validated_data["status"] = receiver_status_choices.rascunho
        try:
            receiver = ReceiverFactory.create(**validated_data)
        except Exception:
            raise ReceiverAlreadyExistsApiException(
                detail=f"A combinação de documento ({validated_data['document']}), chave pix ({validated_data['pix_key']}) e tipo de chave ({validated_data['pix_key_type']}) já existe."
            )

        return receiver

    def update(self, instance, validated_data):
        if instance.status == receiver_status_choices.validado:
            self.partial = True
            self._update_fields = ["email"]
        validated_data["pix_key"] = unmask_pix_key(
            validated_data["pix_key"], validated_data["pix_key_type"]
        )
        validated_data["document"] = convert_to_numerals(validated_data["document"])
        return super().update(instance, validated_data)

    class Meta:
        model = Receiver
