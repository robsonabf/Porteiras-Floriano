from django import forms
from .models import Inscricao

class cadastrocriar(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome', 'email','telefone','empresa_instituicao','mensagem']
