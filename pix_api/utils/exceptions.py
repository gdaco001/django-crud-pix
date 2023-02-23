from rest_framework.exceptions import APIException
from rest_framework import status


class ReceiverAlreadyExistsApiException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Receiver API Exception"
    default_code = "receiver_api_exception"
