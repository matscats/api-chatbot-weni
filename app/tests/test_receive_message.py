from django.test import TestCase

from core.models import Channel, Agent
from core.services import ReceiveMessageService


class ReceiveMessageTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username="jaum", is_available=True)
        self.channel = Channel.objects.create(
            name="Teste", type="mock", config={"token": "teste"}
        )
        self.payload = {
            "contact_id": "1",
            "message": "Olá",
            "name": "João",
            "username": "Jaum",
        }

    def test_receive_message(self):
        """
        Teste para verificar o método de receber mensagens do serviço de mensagens
        """
        service = ReceiveMessageService()
        message = service.receive_message(channel_type="mock", payload=self.payload)

        self.assertEqual(message.direction, "IN")
        self.assertIsNotNone(message.contact)
        self.assertEqual(message.content, "Olá")
