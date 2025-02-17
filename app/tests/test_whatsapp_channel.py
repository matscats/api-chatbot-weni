from django.test import TestCase
from channels import WhatsAppChannel
from unittest.mock import patch, MagicMock


class WhatsAppChannelTest(TestCase):
    def setUp(self):
        self.config = {
            "account_sid": "teste_sid",
            "auth_token": "teste_token",
            "from_number": "+553835351218",
        }

    @patch("channels.whatsapp.Client")
    def test_send_message(self, mock_client):
        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = MagicMock()
        mock_client.return_value = mock_client_instance

        channel = WhatsAppChannel(self.config)

        result = channel.send_message("+551630651351", "Teste")

        self.assertTrue(result)

        mock_client_instance.messages.create.assert_called_once_with(
            body="Teste",
            from_="whatsapp:+553835351218",
            to="whatsapp:+551630651351",
        )

    def test_process_webhook(self):
        payload = {
            "From": "whatsapp:+551630651351",
            "Body": "Olá",
            "ProfileName": "Teste da Silva",
        }

        channel = WhatsAppChannel(self.config)

        result = channel.process_webhook(payload)

        self.assertEqual(result["contact_id"], "+551630651351")
        self.assertEqual(result["message"], "Olá")
        self.assertEqual(result["contact_data"]["name"], "Teste da Silva")
        self.assertEqual(result["contact_data"]["username"], "whatsapp:+551630651351")
