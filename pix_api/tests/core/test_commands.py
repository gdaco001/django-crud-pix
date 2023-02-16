from unittest import mock

import pytest
from apps.core.management.commands.generate_data import Command as GenerateDataCommand

pytestmark = pytest.mark.django_db


@mock.patch("apps.core.factories.ReceiverFactory.create_batch")
def test_generate_data(mocked_create_batch):
    GenerateDataCommand().handle(**{"data_amount": 30})
    mocked_create_batch.assert_called_with(30)


def test_add_arguments():
    command = GenerateDataCommand()
    parser = command.create_parser("test", "create_receivers")
    assert ("data_amount" in [action.dest for action in parser._actions]) is True
