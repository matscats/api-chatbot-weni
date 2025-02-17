from rest_framework.exceptions import APIException


class FailedToReceiveMessage(APIException):
    default_code = "receive_message"
    default_detail = "Houve um erro ao receber a mensagem."


class FailedToSendMessage(APIException):
    default_code = "send_message"
    default_detail = "Houve um erro ao enviar a mensagem."
