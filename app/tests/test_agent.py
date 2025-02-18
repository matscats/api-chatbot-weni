from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import Agent


class AgentAPITest(APITestCase):
    def setUp(self):
        self.agent_data = {
            "username": "teste",
            "password": "teste123",
            "email": "teste@email.com",
            "is_available": True,
        }

        self.agent = Agent.objects.create_user(
            username="agente",
            password="agente123",
            email="agente@email.com",
            is_available=True,
        )

    def test_create_agent(self):
        """
        Veriica a rota de criação do agente.
        """
        url = reverse("agent-list")
        response = self.client.post(url, self.agent_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agent.objects.latest("date_joined").username, "teste")
        self.assertTrue(Agent.objects.latest("date_joined").check_password("teste123"))

    def test_get_agent_list_unauthenticated(self):
        """
        Verifica a rota de listagem de agentes sem estar autenticado.
        """
        url = reverse("agent-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_agent_detail(self):
        """
        Verifica a rota de GET de agentes.
        """
        url = reverse("agent-detail", kwargs={"pk": self.agent.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "agente")
        self.assertEqual(response.data["email"], "agente@email.com")

    def test_update_agent_unauthorized(self):
        """
        Verifica a rota de atualizar agente sem estar autenticado.
        """
        url = reverse("agent-detail", kwargs={"pk": self.agent.pk})
        update_data = {"is_available": False}
        response = self.client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_agent_authorized(self):
        """
        Verifica a rota de atualizar agente.
        """
        self.client.force_authenticate(user=self.agent)
        url = reverse("agent-detail", kwargs={"pk": self.agent.pk})
        update_data = {"is_available": False}
        response = self.client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agent.refresh_from_db()
        self.assertFalse(self.agent.is_available)

    def test_delete_agent_unauthorized(self):
        """
        Verifica a rota de excluir agente sem estar autenticado.
        """
        url = reverse("agent-detail", kwargs={"pk": self.agent.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_agent_authorized(self):
        """
        Verifica a rota de excluir agente.
        """
        self.client.force_authenticate(user=self.agent)
        url = reverse("agent-detail", kwargs={"pk": self.agent.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_agent_invalid_data(self):
        """
        Verifica a criação de cliente sem passar os parâmetros necessários.
        """
        url = reverse("agent-list")
        invalid_data = {"username": "", "password": "teste123"}
        response = self.client.post(url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_not_returned_in_response(self):
        """
        Verifica que a senha do usuário não foi retornada na resposta.
        """
        url = reverse("agent-detail", kwargs={"pk": self.agent.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data)
