from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('register/researcher/', views.register_researcher, name='register_researcher'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/company_investor/', views.register_company_investor, name='register_company_investor'),
    path('register/institution/', views.register_institution, name='register_institution'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('editar-perfil/', views.edit_profile, name='edit_profile'),
    path('contate/', views.contate, name='contact'),
    path('get-cities/', get_cities, name='get_cities'),
    #
    path('galeria/', views.galeria),
    #dashboard e parcerias
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboardpub/', DashboardpublicoView.as_view(), name='dashboardpub'),
    path('buscar-parcerias/', BuscarParceriasView.as_view(), name='buscar_parcerias'),
    path('detalhes-parceria/<int:pk>/', DetalhesParceriaView.as_view(), name='detalhes_parceria'),
    path('ofertar-parcerias/', RequestPartnershipView.as_view(), name='ofertar_parcerias'),
    path('demonstrar-interesse_parceria/<int:partnership_request_id>/', DemonstrarInteresseParceriaView.as_view(),
         name='demonstrar_interesse_parceria'),
    path('firmar-parceria/<int:partnership_request_id>/', FirmarParceriaView.as_view(), name='firmar_parceria'),
    #mentorias
    path('solicitar-mentoria/', SolicitarMentoriaView.as_view(), name='solicitar_mentoria'),
    path('demonstrar-interesse/<int:mentorship_request_id>/', DemonstrarInteresseMentoriaView.as_view(),
         name='demonstrar_interesse'),
    path('firmar-mentoria/<int:mentorship_request_id>/', FirmarMentoriaView.as_view(), name='firmar_mentoria'),
    path('buscar-mentorias/', BuscarMentoriasView.as_view(), name='buscar_mentorias'),
    path('detalhes-mentoria/<int:pk>/', DetalhesMentoriaView.as_view(), name='detalhes_mentoria'),
    #
    path('participacoes-projetos/', ParticipacoesProjetosView.as_view(), name='participacoes_projetos'),
    path('oportunidades-parcerias/', OportunidadesParceriasView.as_view(), name='oportunidades_parcerias'),
    path('vitrine-local/', VitrineLocalView.as_view(), name='vitrine_local'),
    #projetos e usuário
    path('user/<str:username>/', views.user_profile, name='user-profile'),
    path('portfolio/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/<int:project_id>/feedback/', views.add_feedback, name='add-feedback'),
    path('projects/<int:project_id>/partnership/', views.request_partnership, name='request-partnership'),
    path('projects/<int:project_id>/mentorship/', views.request_mentorship, name='request-mentorship'),
    path('participacoes-projetos/', ParticipacoesProjetosView.as_view(), name='participacoes_projetos'),
    #sem implementação
    path('projects/<int:project_id>/impact/', views.view_impact_report, name='view-impact-report'),
    path('projects/<int:project_id>/progress/', views.project_progress, name='project-progress'),
    #
    path('institutions/', views.InstitutionListView.as_view(), name='institution-list'),
    path('institutions/<int:pk>/', views.InstitutionDetailView.as_view(), name='institution-detail'),
    path('projects/<int:project_id>/patent/', views.add_patent, name='add-patent'),
    path('notifications/', views.notifications, name='notifications'),
]
