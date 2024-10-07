from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import TemplateView
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'index.html')


@login_required
def get_cities(request):
    state_id = request.GET.get('state_id')
    cities = Cidade.objects.filter(estado_id=state_id).values('id', 'nome')
    return JsonResponse(list(cities), safe=False)


def contate(request):
    form = InscricaoForm(request.POST or None)  # Atualizado para usar o formulário correto
    if form.is_valid():
        form.save()
        messages.success(request, 'Mensagem enviada com sucesso!')
        return redirect('home')  # Redireciona para a home após sucesso
    return render(request, 'contate-nos.html', {'form': form})


###########
def informatica(request):
    return render(request, 'p_informatica.html')


def galeria(request):
    return render(request, 'galeria.html')


# Dashboard principal
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    # Método para adicionar dados ao contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mentorias solicitadas pelo usuário (ordenadas por data de criação, mais recentes primeiro)
        solicitadas = MentorshipRequest.objects.filter(project__owner=self.request.user.userprofile).order_by(
            '-created_at')
        # Mentorias solicitadas por outros usuários
        solicitacoes_outros = MentorshipRequest.objects.exclude(project__owner=self.request.user.userprofile).order_by(
            '-created_at')

        # Paginação (opcional)
        solicitadas_paginator = Paginator(solicitadas, 5)  # 5 mentorias por página
        solicitacoes_outros_paginator = Paginator(solicitacoes_outros, 5)

        page_number_solicitadas = self.request.GET.get('page_solicitadas')
        page_number_outros = self.request.GET.get('page_outros')

        solicitadas_page_obj = solicitadas_paginator.get_page(page_number_solicitadas)
        solicitacoes_outros_page_obj = solicitacoes_outros_paginator.get_page(page_number_outros)

        # Adicionando os objetos de paginação ao contexto
        context['solicitadas'] = solicitadas_page_obj
        context['solicitacoes_outros'] = solicitacoes_outros_page_obj

        return context


@login_required
def request_mentorship(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = MentoriaForm(request.POST, user_profile=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('project-detail', pk=project.pk)
    else:
        form = MentoriaForm(user_profile=request.user.userprofile)
    return render(request, 'request_mentorship.html', {'form': form, 'project': project})


# Funções comuns a todos os perfis
class BuscarParceriasView(TemplateView):
    template_name = 'buscar_parcerias.html'


class OfertarParceriasView(TemplateView):
    template_name = 'ofertar_parcerias.html'


class ParticipacoesProjetosView(TemplateView):
    template_name = 'participacoes_projetos.html'


class EmitirInteresseView(TemplateView):
    template_name = 'emitir_interesse.html'


# Funcionalidades específicas de Estudantes
@method_decorator(login_required, name='dispatch')
class SolicitarMentoriaView(View):
    template_name = 'solicitar_mentoria.html'

    def get(self, request):
        projects = Project.objects.filter(owner=request.user.userprofile)

        form = MentoriaForm(user_profile=request.user.userprofile)

        context = {
            'projects': projects,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MentoriaForm(request.POST, user_profile=request.user.userprofile)
        if form.is_valid():
            mentorship_request = form.save(commit=False)
            mentorship_request.save()
            return redirect('dashboard')
        else:
            projects = Project.objects.filter(owner=request.user.userprofile)

            context = {
                'projects': projects,
                'form': form,
            }
            return render(request, self.template_name, context)


class DemonstrarInteresseMentoriaView(LoginRequiredMixin, View):
    template_name = 'demonstrar_interesse.html'

    def get(self, request, mentorship_request_id):
        mentorship_request = get_object_or_404(MentorshipRequest, id=mentorship_request_id)
        context = {
            'mentorship_request': mentorship_request,
            'project_owner': mentorship_request.project.owner,  # Acesso ao dono do projeto
        }
        return render(request, self.template_name, context)

    def post(self, request, mentorship_request_id):
        mentorship_request = get_object_or_404(MentorshipRequest, id=mentorship_request_id)

        # Adiciona o mentor interessado
        MentorInterested.objects.create(mentorship_request=mentorship_request, mentor=request.user.userprofile)

        # Redireciona para uma página de confirmação
        return redirect('demonstrar_interesse', mentorship_request_id=mentorship_request.id)


class FirmarMentoriaView(LoginRequiredMixin, View):
    template_name = 'mentoria_detalhes.html'

    def get(self, request, mentorship_request_id):
        # Obtém o pedido de mentoria
        mentorship_request = get_object_or_404(MentorshipRequest, id=mentorship_request_id)

        # Busca o mentor interessado mais recente
        interested_mentor = MentorInterested.objects.filter(mentorship_request=mentorship_request).last()

        context = {
            'mentorship_request': mentorship_request,
            'mentor': interested_mentor.mentor,  # Informações do mentor
        }
        return render(request, self.template_name, context)

    def post(self, request, mentorship_request_id):
        # Obtém o pedido de mentoria
        mentorship_request = get_object_or_404(MentorshipRequest, id=mentorship_request_id)
        mentor_ids = request.POST.getlist('mentores_firmar')
        mentorship_request.is_accepted = True
        mentorship_request.save()
        for mentor_id in mentor_ids:
            mentor = get_object_or_404(UserProfile, id=mentor_id)  # Obtendo o mentor correspondente
            # Adiciona o mentor à lista de mentores associados
            MentorInterested.objects.create(mentorship_request=mentorship_request, mentor=mentor)
        messages.success(request, 'Mentoria firmada com sucesso!')
        return redirect('dashboard')


class MentoriaDetalhesView(LoginRequiredMixin, View):
    template_name = 'mentoria_detalhes.html'

    def get(self, request, mentorship_request_id):
        mentorship_request = get_object_or_404(MentorshipRequest, id=mentorship_request_id)

        context = {
            'mentorship_request': mentorship_request,
        }
        return render(request, self.template_name, context)


class MentoriaConfirmadaView(LoginRequiredMixin, View):
    template_name = 'mentoria_confirmada.html'

    def get(self, request, mentorship_request_id):
        mentorship_request = get_object_or_404(MentorshipRequest, id=mentorship_request_id)

        mentores_confirmados = MentorInterested.objects.filter(mentorship_request=mentorship_request)

        context = {
            'mentorship_request': mentorship_request,
            'mentores_confirmados': mentores_confirmados,
        }
        return render(request, self.template_name, context)


# Funcionalidades específicas de Pesquisadores
class OfertarMentoriasView(TemplateView):
    template_name = 'ofertar_mentorias.html'


# Funcionalidades específicas de Empresas
class AvaliarPotencialView(TemplateView):
    template_name = 'avaliar_potencial.html'


class OportunidadesParceriasView(TemplateView):
    template_name = 'oportunidades_parcerias.html'


# Funcionalidades específicas de Instituições
class GestaoPortfolioView(TemplateView):
    template_name = 'gestao_portfolio.html'


class VitrineLocalView(TemplateView):
    template_name = 'vitrine_local.html'


@login_required
def user_profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    projects = profile.projects.all()
    return render(request, 'user_profile.html', {'profile': profile, 'projects': projects})


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user.userprofile).order_by('-date_created')


@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentorship_requests'] = MentorshipRequest.objects.filter(project=self.object)
        context['partnership_requests'] = PartnershipRequest.objects.filter(project=self.object)
        context['partnership_contracts'] = PartnershipContract.objects.filter(project=self.object)

        return context


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user.userprofile
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'


@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('project-list')


@login_required
def add_feedback(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.project = project
            feedback.user = request.user.userprofile
            feedback.save()
            messages.success(request, 'Feedback enviado com sucesso!')
            return redirect('project-detail', pk=project.pk)
    else:
        form = FeedbackForm()
    return render(request, 'add_feedback.html', {'form': form, 'project': project})

####################

@login_required
def request_partnership(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = PartnershipRequestForm(request.POST)  # Atualizado para usar o formulário correto
        if form.is_valid():
            partnership = form.save(commit=False)
            partnership.project = project
            partnership.partner = request.user.userprofile
            partnership.save()
            messages.success(request, 'Solicitação de parceria enviada com sucesso!')
            return redirect('project-detail', pk=project.pk)
    else:
        form = PartnershipRequestForm()
    return render(request, 'request_partnership.html', {'form': form, 'project': project})


@login_required
def view_impact_report(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    impact_reports = ImpactReport.objects.filter(project=project)
    return render(request, 'impact_report.html', {'project': project, 'impact_reports': impact_reports})


@login_required
def project_progress(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    progress_reports = ProjectProgress.objects.filter(project=project)
    return render(request, 'porteiras/project_progress.html', {'project': project, 'progress_reports': progress_reports})


@method_decorator(login_required, name='dispatch')
class InstitutionListView(ListView):
    model = Institution
    template_name = 'institution_list.html'
    context_object_name = 'institutions'


@method_decorator(login_required, name='dispatch')
class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'institution_detail.html'
    context_object_name = 'institution'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.technologies.all()
        return context


@login_required
def add_patent(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = PatentForm(request.POST)
        if form.is_valid():
            patent = form.save(commit=False)
            patent.project = project
            patent.save()
            messages.success(request, 'Patente adicionada com sucesso!')
            return redirect('project-detail', pk=project.pk)
    else:
        form = PatentForm()
    return render(request, 'add_patent.html', {'form': form, 'project': project})


@login_required
def notifications(request):
    notifications = request.user.userprofile.notifications.filter(is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})


#cadastros
def register_researcher(request):
    if request.method == 'POST':
        form = ResearcherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ResearcherRegistrationForm()
    return render(request, 'register.html', {'form': form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


def register_company_investor(request):
    if request.method == 'POST':
        form = CompanyInvestorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CompanyInvestorRegistrationForm()
    return render(request, 'register.html', {'form': form})


def register_institution(request):
    if request.method == 'POST':
        form = InstitutionRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = InstitutionRegistrationForm()
    return render(request, 'register.html', {'form': form})


#acesso
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def edit_profile(request):
    profile = request.user.userprofile  # Acessa o UserProfile associado ao usuário logado
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile')  # Redireciona para a página de perfil
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})
