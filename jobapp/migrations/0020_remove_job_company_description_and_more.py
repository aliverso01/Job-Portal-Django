# Generated by Django 5.0.2 on 2024-06-15 02:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0019_job_tempo_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='company_description',
        ),
        migrations.RemoveField(
            model_name='job',
            name='company_name',
        ),
    ]
