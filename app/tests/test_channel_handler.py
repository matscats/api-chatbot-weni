from django.test import TestCase
from channels.mock import MockChannel


class MockChannelTest(TestCase):
    def setUp(self):
        self.channel = MockChannel(config={})

    def test_send_message(self):
        """
        Testa o método de enviar mensagens a partir do Mock.
        """
        result = self.channel.send_message(contact_id="1", message="Olá")
        self.assertTrue(result)

    def test_process_webhook(self):
        """
        Testa o método de processar webhooks a partir do Mock.
        """
        payload = {
            "contact_id": "1",
            "message": "Olá",
            "name": "João",
            "username": "Jaum",
        }
        result = self.channel.process_webhook(payload)

        self.assertEqual(result["contact_id"], "1")
        self.assertEqual(result["message"], "Olá")
        self.assertEqual(result["contact_data"]["name"], "João")
        self.assertEqual(result["contact_data"]["username"], "Jaum")
