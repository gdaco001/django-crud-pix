import re

from apps.core.choices import document_type_choices, pix_key_type_choices
from faker import Faker

faker = Faker(locale="pt_BR")


def generate_upper_email():
    return faker.email().upper()


def generate_document_by_type(obj):
    return (
        re.sub("[^0-9]", "", faker.cpf())
        if obj.document_type == document_type_choices.cpf
        else re.sub("[^0-9]", "", faker.cnpj())
    )


def generate_pix_key(obj):
    if obj.pix_key_type == pix_key_type_choices.cpf:
        return re.sub("[^0-9]", "", faker.cpf())
    elif obj.pix_key_type == pix_key_type_choices.cnpj:
        return re.sub("[^0-9]", "", faker.cnpj())
    elif obj.pix_key_type == pix_key_type_choices.telefone:
        return re.sub("[^0-9]", "", faker.cellphone_number())
    elif obj.pix_key_type == pix_key_type_choices.email:
        return faker.email().upper()
    else:
        return faker.uuid4()
