from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from core.models import Channel
from core.services import ReceiveMessageService

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(APIView):
    message_service = ReceiveMessageService()
    permission_classes = [permissions.AllowAny]
    _channel_type = "telegram"

    def post(self, request, token):
        try:
            channel = Channel.objects.get(
                type=self._channel_type, config__token=token, is_active=True
            )

            message = self.message_service.receive_message(
                channel_type=self._channel_type, payload=request.data
            )

            return Response(
                {"status": "success", "message": "Mensagem processada com sucesso"},
                status=200,
            )

        except Channel.DoesNotExist:
            return Response(
                {"error": "Canal não encontrado ou token inválido"}, status=403
            )

        except Exception as e:
            return Response(
                {"error": f"Erro ao processar mensagem: {str(e)}"}, status=400
            )
