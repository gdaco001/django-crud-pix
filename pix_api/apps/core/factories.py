import factory
import factory.fuzzy
from faker import Faker
from apps.core.choices import (
    pix_key_type_choices,
    receiver_status_choices,
    document_type_choices,
)
from apps.core.models import Receiver, Bank, BankAccount
from utils.random_attrs import (
    generate_document_by_type,
    generate_pix_key,
    generate_upper_email,
)

faker = Faker(locale="pt_BR")
factory.Faker._DEFAULT_LOCALE = "pt_BR"


class BankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bank
        django_get_or_create = ("bacen_code",)

    name = factory.Faker("company")
    bacen_code = factory.LazyAttribute(lambda o: faker.numerify(text="###"))
    image_url = factory.Faker("url")


class BankAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankAccount
        django_get_or_create = ("bank",)

    bank = factory.SubFactory(BankFactory)
    agency = factory.LazyAttribute(lambda o: faker.numerify(text="%###"))
    agency_digit = factory.LazyAttribute(lambda o: faker.numerify(text="#"))
    account = factory.LazyAttribute(lambda o: faker.numerify(text="%#######"))
    account_digit = factory.LazyAttribute(lambda o: faker.numerify(text="#"))
    is_active = True


class ReceiverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Receiver

    name = factory.Faker("name")
    pix_key_type = factory.Iterator(pix_key_type_choices.values, getter=lambda c: c)
    pix_key = factory.LazyAttribute(lambda o: generate_pix_key(o))
    email = factory.LazyFunction(generate_upper_email)
    document_type = factory.fuzzy.FuzzyChoice(document_type_choices.values)
    document = factory.LazyAttribute(lambda o: generate_document_by_type(o))
    status = factory.fuzzy.FuzzyChoice(
        [
            receiver_status_choices.validado,
            receiver_status_choices.rascunho,
        ]
    )
    bank_account = factory.SubFactory(BankAccountFactory)
