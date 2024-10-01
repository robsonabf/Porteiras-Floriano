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
        fields = ['title', 'description', 'category', 'status', 'institution', 'start_date', 'end_date', 'funding_required']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
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
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['project', 'comment', 'rating']  # Removido 'user'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
        }
        labels = {
            'comment': 'Comentário',
            'rating': 'Avaliação (1-5)',
        }


class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['project', 'partner_name', 'partner_email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'partner_name': 'Nome do Parceiro',
            'partner_email': 'Email do Parceiro',
            'message': 'Mensagem para o Parceiro',
        }


class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['project', 'mentor', 'message']  # Ajustado para usar 'mentor'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'mentor': 'Mentor',
            'message': 'Mensagem para o Mentor',
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
        fields = ['bio', 'institution_name', 'website', 'linkedin', 'avatar']
        labels = {
            'bio': 'Biografia',
            'institution_name': 'Nome da Instituição',
            'avatar': 'Avatar',
            'website': 'Website',
            'linkedin': 'Linkedin',
        }


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
