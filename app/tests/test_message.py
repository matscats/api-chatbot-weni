from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Message, Contact, Channel, Agent


class MessageAPITest(APITestCase):
    def setUp(self):
        self.agent = Agent.objects.create_user(
            username="agente", password="teste123", email="agente@email.com"
        )

        self.channel = Channel.objects.create(
            name="WhatsApp",
            type="whatsapp",
            config={"api_key": "test_key", "phone_number": "+5511999999999"},
        )

        self.contact = Contact.objects.create(
            external_id="wa_123456", name="João Silva", channel=self.channel
        )

        # Criar uma mensagem
        self.message = Message.objects.create(
            content="Olá",
            contact=self.contact,
            agent=self.agent,
            direction="IN",
            status="RECEIVED",
        )

        self.message_data = {
            "content": "Oi",
            "contact": self.contact.id,
            "agent": self.agent.id,
            "direction": "OUT",
            "status": "PENDING",
        }

    def test_list_messages_unauthorized(self):
        """Teste para verificar que usuários não autenticados não podem listar mensagens"""
        url = reverse("message-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_messages_authorized(self):
        """Teste para listar mensagens com usuário autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("message-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["content"], "Olá")

    def test_create_message_unauthorized(self):
        """Teste para verificar que usuários não autenticados não podem criar mensagens"""
        url = reverse("message-list")
        response = self.client.post(url, self.message_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_message_detail_unauthorized(self):
        """Teste para verificar que usuários não autenticados não podem ver detalhes da mensagem"""
        url = reverse("message-detail", kwargs={"pk": self.message.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_message_detail_authorized(self):
        """Teste para obter detalhes de uma mensagem com usuário autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("message-detail", kwargs={"pk": self.message.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Olá")
        self.assertEqual(response.data["direction"], "IN")

    def test_message_filters(self):
        """Teste para verificar os filtros de mensagem"""
        self.client.force_authenticate(user=self.agent)

        # Criar mais algumas mensagens para testar filtros
        Message.objects.create(
            content="Test outbound message",
            contact=self.contact,
            agent=self.agent,
            direction="OUT",
            status="PENDING",
        )

        # Teste filtro por direction
        url = reverse("message-list") + "?direction=OUT"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        # Teste filtro por status
        url = reverse("message-list") + "?status=RECEIVED"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_message_invalid_data(self):
        """Teste para criar mensagem com dados inválidos"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("message-list")

        invalid_data = {
            "content": "",  # conteúdo vazio
            "contact": self.contact.id,
            "direction": "INVALID",  # direção inválida
            "status": "PENDING",
        }

        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagination(self):
        """Teste para verificar a paginação"""
        self.client.force_authenticate(user=self.agent)

        # Criar mais mensagens
        for i in range(15):  # Criar total de 16 mensagens
            Message.objects.create(
                content=f"Test message {i}",
                contact=self.contact,
                agent=self.agent,
                direction="IN",
                status="RECEIVED",
            )

        url = reverse("message-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 16)
