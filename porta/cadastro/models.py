from django.db import models
from django.contrib.auth.models import User
from .utils import compress_image


"""UserProfile: Garante que o sistema tenha diferentes perfis de usuários (pesquisadores, estudantes, empresas, instituições) com informações específicas para cada tipo.
TechnologyCategory: Permite a categorização das tecnologias para facilitar a organização e busca.
Project: O coração do sistema, permitindo que os usuários cadastrem ideias, projetos e tecnologias, associando informações como estágio, categoria, colaboradores, etc.
Feedback: Facilita a colaboração, onde outros usuários podem fornecer sugestões e feedbacks.
Partnership: Gere parcerias entre projetos e interessados (empresas, investidores, etc.).
Institution: Garante que instituições possam registrar seus portfólios de tecnologias e buscar parcerias.
ImpactReport: Relatórios de impacto para acompanhar o desempenho dos projetos e tecnologias no sistema.
ProjectProgress: Registra o progresso dos projetos ao longo do tempo.
MentorshipRequest: Estudantes ou pesquisadores podem solicitar mentoria em projetos.
PartnershipContract: Formaliza as parcerias com documentos digitais de contratos.
Notification: Mantém os usuários informados sobre eventos importantes no sistema.
Patent: Integração com bases de patentes para verificar a proteção intelectual de uma tecnologia."""


class Inscricao(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    telefone = models.CharField(max_length=20, blank=True)
    empresa_instituicao = models.CharField(max_length=100)
    mensagem = models.CharField(max_length=1000)

    def __str__(self):
        return self.nome


class UserProfile(models.Model):
    USER_TYPES = (
        ('pesquisador', 'Pesquisador'),
        ('estudante', 'Estudante'),
        ('empresa', 'Empresa'),
        ('instituicao', 'Instituição'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=300)
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    bio = models.TextField(null=True, blank=True)
    institution_name = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_user_type_display()}'

    def save(self, *args, **kwargs):
        if self.avatar:
            self.avatar = compress_image(self.avatar)
        super().save(*args, **kwargs)


class TechnologyCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Project(models.Model):
    STAGE_CHOICES = (
        ('ideia', 'Ideia'),
        ('em_progresso', 'Em Progresso'),
        ('completo', 'Completo'),
    )

    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('concluido', 'Concluído'),
    )

    location_state = models.ForeignKey('Estado', on_delete=models.SET_NULL, null=True)
    location_city = models.ForeignKey('Cidade', on_delete=models.SET_NULL, null=True)
    logo = models.ImageField(upload_to='projetos_logos/', null=True, blank=True)
    needs = models.ManyToManyField('Need', related_name='projects', blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ativo')
    category = models.ForeignKey(TechnologyCategory, on_delete=models.SET_NULL, null=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    funding_required = models.BooleanField(default=False)
    goals = models.TextField(null=True, blank=True)
    resources_needed = models.TextField(null=True, blank=True)
    collaborators = models.ManyToManyField(UserProfile, related_name='collaborations', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    keywords = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.logo:
            self.logo = compress_image(self.logo)
        super().save(*args, **kwargs)


class Feedback(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)  # Campo de comentário
    rating = models.IntegerField(null=True, blank=True)  # Campo de avaliação (1 a 5)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user} on {self.project}"


class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(null=True, blank=True)
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to='institution_logos/', null=True, blank=True)
    technologies = models.ManyToManyField(Project, related_name='institution_projects', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.logo:
            self.logo = compress_image(self.logo)
        super().save(*args, **kwargs)


class PartnershipRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='partnership_requests')
    message = models.TextField()  # Mensagem enviada pelo solicitante
    is_accepted = models.BooleanField(default=False)  # Indicador se a parceria foi aceita
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação da solicitação

    def __str__(self):
        return f'Parceria solicitada para {self.project.title}'

    def accept_partner(self, partner):
         # Verificar se o parceiro já demonstrou interesse para evitar duplicidades
        if not PartnerInterested.objects.filter(partnership_request=self, partner=partner).exists():
            PartnerInterested.objects.create(partnership_request=self, partner=partner)

    def has_interested_partners(self):
        return self.interested_partners.exists()  # Verificar se há parceiros interessados


class PartnerInterested(models.Model):
    partnership_request = models.ForeignKey(PartnershipRequest, on_delete=models.CASCADE, related_name='interested_partners')
    partner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='partnership_requests_made')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Parceiro {self.partner.user.username} interessado no projeto {self.partnership_request.project.title}'


class MentorshipRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='mentorship_requests')
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mentorship request for {self.project.title}'

    def accept_mentor(self, mentor):
        # Verifica se o mentor já está interessado para evitar duplicidade
        if not MentorInterested.objects.filter(mentorship_request=self, mentor=mentor).exists():
            MentorInterested.objects.create(mentorship_request=self, mentor=mentor)

    def has_interested_mentors(self):
        return self.interested_mentors.exists()  # Verifica se há mentores interessados


class MentorInterested(models.Model):
    mentorship_request = models.ForeignKey(MentorshipRequest, on_delete=models.CASCADE, related_name='interested_mentors')
    mentor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='interested_requests')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mentor {self.mentor.user.username} interested in {self.mentorship_request.project.title}'


class PartnershipContract(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='partnership_contracts')
    partner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    contract_details = models.TextField()
    date_signed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contract for {self.project.title} with {self.partner.user.username}'


class Regiao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Estado(models.Model):
    codigo_uf = models.IntegerField()
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Cidade(models.Model):
    codigo = models.BigIntegerField()
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Need(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ImpactReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='impact_reports')
    views = models.IntegerField(default=0)
    contacts = models.IntegerField(default=0)
    partnerships = models.IntegerField(default=0)
    date_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Impact Report for {self.project.title}'


class ProjectProgress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='progress_updates')
    progress_report = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Progress for {self.project.title}'


class Notification(models.Model):
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.user.username}'


class Patent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='patents')
    patent_number = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    filing_date = models.DateField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return f'Patent {self.patent_number} for {self.project.title}'
