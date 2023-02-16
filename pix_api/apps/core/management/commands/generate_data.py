from django.core.management.base import BaseCommand
from apps.core.factories import ReceiverFactory


class Command(BaseCommand):
    help = "Create a bunch of receivers"

    def add_arguments(self, parser):
        parser.add_argument("data_amount", type=int)

    def handle(self, *args, **kwargs):
        data_amount = kwargs["data_amount"]
        ReceiverFactory.create_batch(data_amount)
