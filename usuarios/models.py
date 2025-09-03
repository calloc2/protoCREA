from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    PERMISSAO_CHOICES = [
        ('visualizador', 'Visualizador'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
        ('admin', 'Administrador'),
    ]
    
    UNIDADE_CHOICES = [
        ('sede_palmas', 'SEDE - PALMAS'),
        ('inspetoria_araguaina', 'INSPETORIA DE ARAGUAÍNA'),
        ('inspetoria_augustinopolis', 'INSPETORIA DE AUGUSTINÓPOLIS'),
        ('inspetoria_dianopolis', 'INSPETORIA DE DIANÓPOLIS'),
        ('inspetoria_guarai', 'INSPETORIA DE GUARAÍ'),
        ('inspetoria_gurupi', 'INSPETORIA DE GURUPI'),
        ('inspetoria_paraiso_tocantins', 'INSPETORIA DE PARAÍSO DO TOCANTINS'),
        ('inspetoria_porto_nacional', 'INSPETORIA DE PORTO NACIONAL'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cpf = models.CharField("CPF", max_length=14, unique=True, help_text="000.000.000-00")
    telefone = models.CharField("Telefone", max_length=15, blank=True, help_text="(00) 00000-0000")
    registro_profissional = models.CharField("Registro Profissional", max_length=20, blank=True, help_text="Número do registro no CREA")
    empresa = models.CharField("Empresa/Instituição", max_length=200, blank=True)
    cargo = models.CharField("Cargo/Função", max_length=100, blank=True)
    permissao = models.CharField("Nível de Permissão", max_length=20, choices=PERMISSAO_CHOICES, default='visualizador')
    pode_publicar = models.BooleanField("Pode Publicar Atas", default=False)
    local = models.CharField(
        "Local de Trabalho",
        max_length=30,
        choices=UNIDADE_CHOICES,
        default='sede_palmas',
        help_text="Unidade do CREA-TO onde o usuário trabalha"
    )
    
    conta_aprovada = models.BooleanField("Conta Aprovada", default=False)
    data_aprovacao = models.DateTimeField("Data de Aprovação", null=True, blank=True)
    aprovado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_aprovados'
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)
    ultimo_acesso = models.DateTimeField("Último Acesso", null=True, blank=True)

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"

    @property
    def is_approved(self):
        return self.conta_aprovada

    @property
    def can_publish(self):
        return self.is_approved and self.pode_publicar
    
    @property
    def can_edit(self):
        return self.is_approved and self.permissao in ['editor', 'publicador', 'admin']
