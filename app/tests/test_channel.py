from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Channel, Agent


class ChannelAPITest(APITestCase):
    def setUp(self):
        self.agent = Agent.objects.create_user(
            username="agente", password="teste123", email="agente@email.com"
        )

        self.channel_data = {
            "name": "WhatsApp",
            "type": "whatsapp",
            "config": {"api_key": "test_key", "phone_number": "+5511999999999"},
        }

        self.channel = Channel.objects.create(
            name="Telegram",
            type="telegram",
            config={
                "bot_token": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
                "webhook_url": "https://api.telegram.org/bot",
            },
        )

    def test_list_channels(self):
        """Teste para listar todos os canais"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("channel-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Telegram")
        self.assertEqual(response.data[0]["type"], "telegram")

    def test_get_channel_detail(self):
        """Teste para obter detalhes de um canal específico"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("channel-detail", kwargs={"pk": self.channel.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Telegram")
        self.assertEqual(response.data["type"], "telegram")

    def test_list_channels_with_multiple_items(self):
        """Teste para listar múltiplos canais"""
        self.client.force_authenticate(user=self.agent)
        Channel.objects.create(
            name="WhatsApp",
            type="whatsapp",
            config={"api_key": "whatsapp_key", "phone_number": "+5511888888888"},
        )

        url = reverse("channel-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_channel_detail_invalid_id(self):
        """Teste para tentar acessar um canal com ID inválido"""
        self.client.force_authenticate(user=self.agent)
        url = reverse(
            "channel-detail", kwargs={"pk": "123e4567-e89b-12d3-a456-426614174000"}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
