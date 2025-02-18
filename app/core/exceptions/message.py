from rest_framework.exceptions import APIException


class FailedToReceiveMessage(APIException):
    """
    Erro padrão para mensagens que falharam ao serem recebidas.
    """

    default_code = "receive_message"
    default_detail = "Houve um erro ao receber a mensagem."


class FailedToSendMessage(APIException):
    """
    Erro padrão para mensagens que falharam ao serem enviadas.
    """

    default_code = "send_message"
    default_detail = "Houve um erro ao enviar a mensagem."
