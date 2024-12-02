from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project, MentorshipRequest, MentorInterested, UserProfile  # Importe UserProfile


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

        # Criar UserProfile para o usuário
        self.user_profile = UserProfile.objects.create(user=self.user, nome='Test User',
                                                       user_type='pesquisador')  # Preencha os campos obrigatórios

        self.client.login(username='testuser', password='12345')

    def test_dashboard_view_status_code(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_view_contains_mentorship_requests(self):
        # Crie um projeto e uma solicitação de mentoria para o usuário logado
        project = Project.objects.create(owner=self.user_profile, title='Projeto Teste',
                                         description='Descrição do projeto', stage='em_progresso')
        MentorshipRequest.objects.create(project=project)

        response = self.client.get(reverse('dashboard'))

        # Usar len() para contar o número de itens
        self.assertIn('solicitadas', response.context)
        self.assertEqual(len(response.context['solicitadas']), 1)  # Usar len() em vez de count()

    def test_dashboard_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')
