from django.test import TestCase

from core.models import Channel, Agent, Contact
from core.services import SendMessageService


class SendMessageTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username="jaum", is_available=True)
        self.channel = Channel.objects.create(
            name="Teste", type="mock", config={"token": "teste"}
        )
        self.contact = Contact.objects.create(
            external_id="1", name="fulano", channel=self.channel
        )

    def test_receive_message(self):
        """
        Teste para verificar o envio de mensagens no serviço de mensagens
        """
        service = SendMessageService()
        message = service.send_message(
            contact_id=self.contact.id, content="Olá", agent_id=self.agent.id
        )

        self.assertEqual(message.direction, "OUT")
        self.assertIsNotNone(message.contact)
        self.assertEqual(message.content, "Olá")
