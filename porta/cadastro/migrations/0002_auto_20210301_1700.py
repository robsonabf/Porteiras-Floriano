# Generated by Django 3.1.6 on 2021-03-01 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscricao',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]