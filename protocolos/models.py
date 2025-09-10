from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

class LocalArmazenamento(models.Model):
    """Modelo para definir o local físico de armazenamento dos protocolos"""
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
    
    local_armazenamento = models.CharField(
        "Local de Armazenamento",
        max_length=30,
        choices=UNIDADE_CHOICES,
        default='sede_palmas',
        help_text="Unidade do CREA-TO onde está o armazenamento"
    )
    
    armario = models.CharField(
        "Armário", 
        max_length=50,
        help_text="Número do armário (apenas números)"
    )
    
    prateleira = models.CharField(
        "Prateleira", 
        max_length=50,
        help_text="Número da prateleira (apenas números)"
    )
    
    caixa = models.CharField(
        "Caixa", 
        max_length=50,
        help_text="Número da caixa (apenas números)"
    )
    
    class Meta:
        verbose_name = "Local de Armazenamento"
        verbose_name_plural = "Locais de Armazenamento"
        unique_together = ['local_armazenamento', 'armario', 'prateleira', 'caixa']
        ordering = ['local_armazenamento', 'armario', 'prateleira', 'caixa']

    def __str__(self):
        return f"{self.get_local_armazenamento_display()} - Armário {self.armario} - Prateleira {self.prateleira} - Caixa {self.caixa}"

class TipoDocumento(models.Model):
    """Modelo para definir os tipos de documentos por categoria de processo"""
    CATEGORIA_CHOICES = [
        ('finalistico_pf', 'Processo Finalístico - Pessoa Física'),
        ('finalistico_pj', 'Processo Finalístico - Pessoa Jurídica'),
        ('administrativo', 'Processo Administrativo'),
    ]
    
    categoria = models.CharField(
        "Categoria do Processo",
        max_length=20,
        choices=CATEGORIA_CHOICES,
        help_text="Categoria do processo ao qual este tipo de documento pertence"
    )
    
    nome = models.CharField(
        "Nome do Documento",
        max_length=100,
        help_text="Nome do tipo de documento"
    )
    
    ativo = models.BooleanField(
        "Ativo",
        default=True,
        help_text="Se este tipo de documento está ativo"
    )
    
    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documentos"
        ordering = ['categoria', 'nome']
        unique_together = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.get_categoria_display()} - {self.nome}"

class Documento(models.Model):
    """Modelo para armazenar documentos associados a um protocolo"""
    protocolo = models.ForeignKey(
        'Protocolo',
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name="Protocolo"
    )
    
    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Documento"
    )
    
    observacoes = models.TextField(
        "Observações",
        blank=True,
        help_text="Observações sobre este documento"
    )
    
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.protocolo.numero} - {self.tipo_documento.nome}"

class Protocolo(models.Model):
    TIPO_CHOICES = [
        ('finalistico_pf', 'Processo Finalístico - Pessoa Física'),
        ('finalistico_pj', 'Processo Finalístico - Pessoa Jurídica'),
        ('administrativo', 'Processo Administrativo'),
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
    
    numero = models.CharField(
        "Número de Protocolo", 
        max_length=50, 
        unique=True,
        help_text="Número único do protocolo"
    )
    
    data_emissao = models.DateField(
        "Data de Emissão", 
        auto_now_add=True,
        help_text="Data de criação do protocolo"
    )
    
    cpf_cnpj = models.CharField(
        "CPF/CNPJ", 
        max_length=18,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}|\d{14}$',
                message='CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'
            )
        ],
        help_text="CPF (11 dígitos) ou CNPJ (14 dígitos) - obrigatório para processos finalísticos"
    )
    
    tipo = models.CharField(
        "Tipo de Processo", 
        max_length=20, 
        choices=TIPO_CHOICES,
        help_text="Tipo de processo a ser protocolado"
    )
    

    
    armario = models.CharField(
        "Armário",
        max_length=10,
        blank=True,
        help_text="Número do armário (apenas números)"
    )
    
    prateleira = models.CharField(
        "Prateleira",
        max_length=10,
        blank=True,
        help_text="Número da prateleira (apenas números)"
    )
    
    caixa = models.CharField(
        "Caixa",
        max_length=10,
        blank=True,
        help_text="Número da caixa (apenas números)"
    )
    
    unidade_crea = models.CharField(
        "Unidade CREA-TO",
        max_length=30,
        choices=UNIDADE_CHOICES,
        default='sede_palmas',
        help_text="Unidade do CREA-TO responsável pelo protocolo"
    )
    
    observacoes = models.TextField(
        "Observações", 
        blank=True,
        help_text="Observações adicionais sobre o protocolo"
    )
    
    protocolo_sitac = models.CharField(
        "Protocolo SITAC", 
        max_length=50, 
        blank=True,
        null=True,
        help_text="Número de protocolo retornado pela API do SITAC"
    )
    
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='protocolos_criados',
        verbose_name="Criado por"
    )
    
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-data_emissao", "-criado_em"]
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"

    def __str__(self):
        return f"Protocolo {self.numero} - {self.get_tipo_display()}"
    
    @property
    def local_armazenamento_completo(self):
        """Retorna o local de armazenamento completo concatenado"""
        if self.armario and self.prateleira and self.caixa:
            return f"{self.get_unidade_crea_display()} - Armário {self.armario} - Prateleira {self.prateleira} - Caixa {self.caixa}"
        else:
            return "Local não definido"
    
    @property
    def identificador_local(self):
        """Retorna identificador único concatenando ID do protocolo com local"""
        if self.armario and self.prateleira and self.caixa:
            return f"PROT-{self.id}-{self.armario}-{self.prateleira}-{self.caixa}"
        else:
            return f"PROT-{self.id}"

    def clean(self):
        """Validação personalizada para CPF/CNPJ e campos de armazenamento"""
        # Validação de CPF/CNPJ baseada no tipo de processo
        if self.tipo in ['finalistico_pf', 'finalistico_pj']:
            if not self.cpf_cnpj:
                raise ValidationError({
                    'cpf_cnpj': 'CPF/CNPJ é obrigatório para processos finalísticos'
                })
            
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', self.cpf_cnpj)
            
            if self.tipo == 'finalistico_pf' and len(cpf_cnpj_limpo) != 11:
                raise ValidationError({
                    'cpf_cnpj': 'CPF deve ter 11 dígitos para processos finalísticos de pessoa física'
                })
            elif self.tipo == 'finalistico_pj' and len(cpf_cnpj_limpo) != 14:
                raise ValidationError({
                    'cpf_cnpj': 'CNPJ deve ter 14 dígitos para processos finalísticos de pessoa jurídica'
                })
        elif self.tipo == 'administrativo' and self.cpf_cnpj:
            raise ValidationError({
                'cpf_cnpj': 'CPF/CNPJ não deve ser informado para processos administrativos'
            })
        
        # Validação dos campos de armazenamento
        if self.armario and not self.armario.isdigit():
            raise ValidationError({
                'armario': 'O armário deve conter apenas números.'
            })
        
        if self.prateleira and not self.prateleira.isdigit():
            raise ValidationError({
                'prateleira': 'A prateleira deve conter apenas números.'
            })
        
        if self.caixa and not self.caixa.isdigit():
            raise ValidationError({
                'caixa': 'A caixa deve conter apenas números.'
            })
    
    def save(self, *args, **kwargs):
        """Sobrescreve save para aplicar validações"""
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def cpf_cnpj_formatado(self):
        """Retorna o CPF/CNPJ formatado"""
        if not self.cpf_cnpj:
            return "Não informado"
        
        cpf_cnpj_limpo = re.sub(r'[^\d]', '', self.cpf_cnpj)
        if len(cpf_cnpj_limpo) == 11:
            return f"{cpf_cnpj_limpo[:3]}.{cpf_cnpj_limpo[3:6]}.{cpf_cnpj_limpo[6:9]}-{cpf_cnpj_limpo[9:]}"
        elif len(cpf_cnpj_limpo) == 14:
            return f"{cpf_cnpj_limpo[:2]}.{cpf_cnpj_limpo[2:5]}.{cpf_cnpj_limpo[5:8]}/{cpf_cnpj_limpo[8:12]}-{cpf_cnpj_limpo[12:]}"
        return self.cpf_cnpj
