from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome', 'email', 'telefone', 'empresa_instituicao', 'mensagem']
        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'telefone': 'Telefone',
            'empresa_instituicao': 'Empresa/Instituição',
            'mensagem': 'Mensagem',
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'logo',
            'category',
            'status',
            'institution',
            'start_date',
            'end_date',
            'funding_required',
            'location_state',
            'location_city',
            'needs',
            'stage',
            'keywords',
        ]

        # Adicionando widgets com a classe form-control
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'funding_required': forms.CheckboxInput(),
            'location_state': forms.Select(attrs={'class': 'form-control'}),
            'location_city': forms.Select(attrs={'class': 'form-control'}),
            'needs': forms.CheckboxSelectMultiple(),  # Não precisa de form-control
            'stage': forms.Select(attrs={'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Palavras-chave separadas por vírgulas'}),
        }

        labels = {
            'title': 'Título do Projeto',
            'description': 'Descrição',
            'category': 'Categoria',
            'status': 'Status do Projeto',
            'institution': 'Instituição Relacionada',
            'start_date': 'Data de Início',
            'end_date': 'Data de Término',
            'funding_required': 'Financiamento Necessário',
            'location_state': 'Estado do Projeto',
            'location_city': 'Município do Projeto',
            'needs': 'Necessidades',
            'stage': 'Fase de Desenvolvimento',
            'keywords': 'Palavras-chave para Busca',
            'logo': 'Logo ou Imagem do Projeto',
        }

    def clean_keywords(self):
        keywords = self.cleaned_data.get('keywords')
        keywords = ', '.join([kw.strip() for kw in keywords.split(',') if kw.strip()])
        return keywords


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
        }
        labels = {
            'comment': 'Comentário',
            'rating': 'Avaliação (1-5)',
        }


class MentoriaForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['project', 'message']
        labels = {
            'project': 'Projeto',
            'message': 'Mensagem para o Mentor',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile')  # Retire o user_profile da kwargs
        super().__init__(*args, **kwargs)

        # Filtrar os projetos do usuário logado
        self.fields['project'].queryset = Project.objects.filter(owner=user_profile)


class DemonstrarInteresseForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['project', 'message']
        labels = {
            'project': 'Projeto para Mentoria',
            'message': 'Mensagem para o dono do Projeto',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class ResearcherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Criar perfil de pesquisador
            UserProfile.objects.create(user=user, user_type='pesquisador')
        return user


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Criar perfil de estudante
            UserProfile.objects.create(user=user, user_type='estudante')
        return user


class CompanyInvestorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Criar perfil de empresa/investidor
            UserProfile.objects.create(user=user, user_type='empresa')
        return user


class InstitutionRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Criar perfil de instituição
            UserProfile.objects.create(user=user, user_type='instituicao')
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nome', 'bio', 'institution_name', 'website', 'linkedin', 'avatar']
        labels = {
            'nome': 'Nome Completo',
            'bio': 'Biografia',
            'institution_name': 'Nome da Instituição',
            'avatar': 'Avatar',
            'website': 'Website',
            'linkedin': 'Linkedin',
        }


class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escreva sua mensagem...'}),
        }
        labels = {
            'message': 'Mensagem para o Parceiro',
        }

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)  # Recebemos o user_profile se for necessário
        super().__init__(*args, **kwargs)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'content', 'is_read']  # Ajustado para 'content'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'recipient': 'Destinatário',
            'content': 'Mensagem',
            'is_read': 'Lida',
        }


class ImpactReportForm(forms.ModelForm):
    class Meta:
        model = ImpactReport
        fields = ['project', 'views', 'contacts', 'partnerships']  # Ajustado para incluir os campos corretos
        labels = {
            'views': 'Visualizações',
            'contacts': 'Contatos',
            'partnerships': 'Parcerias',
        }


class PatentForm(forms.ModelForm):
    class Meta:
        model = Patent
        fields = ['project', 'patent_number', 'filing_date', 'abstract']  # Ajustado para incluir 'abstract'
        widgets = {
            'filing_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'patent_number': 'Número da Patente',
            'abstract': 'Resumo da Patente',  # Ajustado para 'abstract'
            'filing_date': 'Data de Registro',
        }
