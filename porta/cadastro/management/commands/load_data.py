import json
from django.core.management.base import BaseCommand
from cadastro.models import Estado, Cidade, Regiao
import json
import os


class Command(BaseCommand):
    help = 'Carrega dados de Estados, Cidades e Regiões a partir de arquivos JSON'

    def handle(self, *args, **kwargs):
        # Obtém o diretório do script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Limpa as tabelas
        Regiao.objects.all().delete()
        Estado.objects.all().delete()
        Cidade.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Tabelas limpas com sucesso.'))
        # Carregar Regiões
        with open(os.path.join(base_dir, 'regioes.json'), 'r', encoding='utf-8') as regioes_file:
            regioes_data = json.load(regioes_file)
            for item in regioes_data['data']:
                Regiao.objects.get_or_create(id=item['Id'], nome=item['Nome'])
            self.stdout.write(self.style.SUCCESS('Regiões carregadas com sucesso.'))

        # Carregar Estados
        with open(os.path.join(base_dir, 'estados.json'), 'r', encoding='utf-8') as estados_file:
            estados_data = json.load(estados_file)
            for item in estados_data['data']:
                regiao = Regiao.objects.get(id=item['Regiao'])
                Estado.objects.get_or_create(
                    id=item['Id'],
                    codigo_uf=item['CodigoUf'],
                    nome=item['Nome'],
                    uf=item['Uf'],
                    regiao=regiao
                )
            self.stdout.write(self.style.SUCCESS('Estados carregados com sucesso.'))

        # Carregar Cidades
        with open(os.path.join(base_dir, 'municipios.json'), 'r', encoding='utf-8') as municipios_file:
            municipios_data = json.load(municipios_file)
            for item in municipios_data['data']:
                estado = Estado.objects.get(uf=item['Uf'])
                Cidade.objects.get_or_create(
                    id=item['Id'],
                    codigo=item['Codigo'],
                    nome=item['Nome'],
                    estado=estado
                )
            self.stdout.write(self.style.SUCCESS('Cidades carregadas com sucesso.'))
