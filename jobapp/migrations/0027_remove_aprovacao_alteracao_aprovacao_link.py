# Generated by Django 5.0.2 on 2024-06-16 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0026_aprovacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aprovacao',
            name='alteracao',
        ),
        migrations.AddField(
            model_name='aprovacao',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
