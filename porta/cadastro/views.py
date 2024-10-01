from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *


def home(request):
    return render(request, 'index.html')


def contate(request):
    form = InscricaoForm(request.POST or None)  # Atualizado para usar o formulário correto
    if form.is_valid():
        form.save()
        messages.success(request, 'Mensagem enviada com sucesso!')
        return redirect('home')  # Redireciona para a home após sucesso
    return render(request, 'contate-nos.html', {'form': form})


def informatica(request):
    return render(request, 'p_informatica.html')


def galeria(request):
    return render(request, 'galeria.html')


@login_required
def dashboard(request):
    projects = Project.objects.filter(owner=request.user.userprofile)
    return render(request, 'porteiras/dashboard.html', {'projects': projects})


@login_required
def user_profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    projects = profile.projects.all()
    return render(request, 'porteiras/user_profile.html', {'profile': profile, 'projects': projects})


class ProjectListView(ListView):
    model = Project
    template_name = 'projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(stage='idea').order_by('-date_created')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'porteiras/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback.objects.filter(project=self.object)
        context['partnerships'] = Partnership.objects.filter(project=self.object)
        context['mentorship_requests'] = MentorshipRequest.objects.filter(project=self.object)
        return context


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.userprofile
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'porteiras/project_confirm_delete.html'
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
    return render(request, 'porteiras/add_feedback.html', {'form': form, 'project': project})


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
    return render(request, 'porteiras/request_partnership.html', {'form': form, 'project': project})


@login_required
def request_mentorship(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            mentorship_request = form.save(commit=False)
            mentorship_request.project = project
            mentorship_request.mentor = request.user.userprofile
            mentorship_request.save()
            messages.success(request, 'Solicitação de mentoria enviada com sucesso!')
            return redirect('project-detail', pk=project.pk)
    else:
        form = MentorshipRequestForm()
    return render(request, 'porteiras/request_mentorship.html', {'form': form, 'project': project})


@login_required
def view_impact_report(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    impact_reports = ImpactReport.objects.filter(project=project)
    return render(request, 'porteiras/impact_report.html', {'project': project, 'impact_reports': impact_reports})


@login_required
def project_progress(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    progress_reports = ProjectProgress.objects.filter(project=project)
    return render(request, 'porteiras/project_progress.html', {'project': project, 'progress_reports': progress_reports})


class InstitutionListView(ListView):
    model = Institution
    template_name = 'porteiras/institution_list.html'
    context_object_name = 'institutions'


class InstitutionDetailView(DetailView):
    model = Institution
    template_name = 'porteiras/institution_detail.html'
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
    return render(request, 'porteiras/add_patent.html', {'form': form, 'project': project})


@login_required
def notifications(request):
    notifications = request.user.userprofile.notifications.filter(is_read=False)
    return render(request, 'porteiras/notifications.html', {'notifications': notifications})


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
            return redirect('profile_view')  # Redireciona para a página de perfil
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})
