from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from core.services import ReceiveMessageService

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class BaseWebhookView(APIView):
    message_service = ReceiveMessageService()
    permission_classes = [permissions.AllowAny]
    channel_type: str = None

    def post(self, request):
        try:
            self.message_service.receive_message(
                channel_type=self.channel_type, payload=request.data
            )

            return Response(
                {"status": "success", "message": "Mensagem processada com sucesso"},
                status=200,
            )

        except Exception as e:
            return Response(
                {"error": f"Erro ao processar mensagem: {str(e)}"}, status=400
            )
