# Generated by Django 4.1.3 on 2024-10-09 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0011_mentorinterested_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerinterested',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partnerinterested',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
