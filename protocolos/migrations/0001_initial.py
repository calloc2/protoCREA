# Generated manually for protocolos app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Protocolo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(help_text='Número único do protocolo', max_length=50, unique=True, verbose_name='Número de Protocolo')),
                ('data_emissao', models.DateField(auto_now_add=True, help_text='Data de criação do protocolo', verbose_name='Data de Emissão')),
                ('cpf_cnpj', models.CharField(help_text='CPF (11 dígitos) ou CNPJ (14 dígitos)', max_length=18, validators=[django.core.validators.RegexValidator(message='CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos', regex='^\\d{11}|\\d{14}$')], verbose_name='CPF/CNPJ')),
                ('tipo', models.CharField(choices=[('profissional', 'Profissional'), ('empresa', 'Empresa')], help_text='Tipo de pessoa física ou jurídica', max_length=15, verbose_name='Tipo')),
                ('local_armazenamento', models.CharField(help_text='Ex: CAIXA X, FILEIRA X, FACE X', max_length=100, verbose_name='Local de Armazenamento')),
                ('observacoes', models.TextField(blank=True, help_text='Observações adicionais sobre o protocolo', verbose_name='Observações')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='protocolos_criados', to='usuarios.perfilusuario', verbose_name='Criado por')),
            ],
            options={
                'verbose_name': 'Protocolo',
                'verbose_name_plural': 'Protocolos',
                'ordering': ['-data_emissao', '-criado_em'],
            },
        ),
    ]
