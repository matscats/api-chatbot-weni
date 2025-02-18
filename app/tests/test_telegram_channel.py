from django.test import TestCase
from channels import TelegramChannel
from unittest.mock import patch, AsyncMock, MagicMock


class TelegramChannelTest(TestCase):
    def setUp(self):
        self.config = {"token": "test_token"}
        self.channel = TelegramChannel(self.config)

    @patch("asyncio.run")
    def test_send_message(self, mock_run):
        """
        Testa o envio de mensagens para o canal do telegram a partir de mock.
        """
        mock_run.return_value = None

        result = self.channel.send_message("123", "Teste")

        self.assertTrue(result)

    def test_process_webhook(self):
        """
        Testa o processamento do webhook do telegram a partir de mock.
        """
        payload = {
            "message": {"chat": {"id": 123, "first_name": "Teste"}, "text": "Oi"}
        }

        result = self.channel.process_webhook(payload)

        self.assertEqual(result["contact_id"], "123")
        self.assertEqual(result["message"], "Oi")
