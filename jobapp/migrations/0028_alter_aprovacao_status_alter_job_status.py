# Generated by Django 5.0.2 on 2024-06-18 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0027_remove_aprovacao_alteracao_aprovacao_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprovacao',
            name='status',
            field=models.CharField(choices=[('1', 'Buscando Profissional'), ('2', 'Em andamento'), ('3', 'Aprovação do Cliente'), ('4', 'Solicitado Alteração'), ('5', 'Aguardando Pagamento'), ('6', 'Finalizado'), ('7', 'Correção Enviada')], max_length=1),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('1', 'Buscando Profissional'), ('2', 'Em andamento'), ('3', 'Aprovação do Cliente'), ('4', 'Solicitado Alteração'), ('5', 'Aguardando Pagamento'), ('6', 'Finalizado'), ('7', 'Correção Enviada')], default='1', max_length=1),
        ),
    ]
