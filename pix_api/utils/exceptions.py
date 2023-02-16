from rest_framework.exceptions import APIException


class ReceiverApiException(APIException):
    status_code = 500
    default_detail = "Receiver API Exception"
    default_code = "receiver_api_exception"
