from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Contact, Channel, Agent


class ContactAPITest(APITestCase):
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
            external_id="wa_123456", name="Joao Silva", channel=self.channel
        )

        self.contact_data = {
            "external_id": "wa_654321",
            "name": "Joana Oliveira",
            "channel": self.channel.id,
        }

    def test_list_contacts_unauthorized(self):
        """Teste para verificar que usuários não autenticados não podem listar contatos"""
        url = reverse("contact-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_contacts_authorized(self):
        """Teste para listar todos os contatos com usuário autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("contact-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Joao Silva")
        self.assertEqual(response.data[0]["external_id"], "wa_123456")

    def test_get_contact_detail_unauthorized(self):
        """Teste para verificar que usuários não autenticados não podem ver detalhes do contato"""
        url = reverse("contact-detail", kwargs={"pk": self.contact.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_contact_detail_authorized(self):
        """Teste para obter detalhes de um contato específico com usuário autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("contact-detail", kwargs={"pk": self.contact.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Joao Silva")
        self.assertEqual(response.data["external_id"], "wa_123456")

    def test_create_contact_not_allowed(self):
        """Teste para verificar que não é possível criar um contato via API mesmo autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("contact-list")
        response = self.client.post(url, self.contact_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_contact_not_allowed(self):
        """Teste para verificar que não é possível atualizar um contato via API mesmo autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("contact-detail", kwargs={"pk": self.contact.pk})
        update_data = {"name": "Updated Name"}

        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_contact_not_allowed(self):
        """Teste para verificar que não é possível deletar um contato via API mesmo autenticado"""
        self.client.force_authenticate(user=self.agent)
        url = reverse("contact-detail", kwargs={"pk": self.contact.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_contacts_with_multiple_items(self):
        """Teste para listar múltiplos contatos com usuário autenticado"""
        self.client.force_authenticate(user=self.agent)

        Contact.objects.create(
            external_id="wa_789012", name="Alice Smith", channel=self.channel
        )

        url = reverse("contact-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unique_external_id_per_channel(self):
        """Teste para verificar a unicidade do external_id por canal"""
        with self.assertRaises(Exception):
            Contact.objects.create(
                external_id="wa_123456",
                name="João Segundo",
                channel=self.channel,
            )
