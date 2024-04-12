from django.db import models
from django.contrib.auth.models import Permission


class Inscricao(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    telefone = models.CharField(max_length=20, blank=True)
    empresa_instituicao = models.CharField(max_length=100)
    mensagem = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.nome
