from django.contrib import admin
from .models import Protocolo

@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'tipo', 'cpf_cnpj_formatado', 'data_emissao', 
        'unidade_crea', 'armario', 'prateleira', 'caixa', 'protocolo_sitac', 'criado_por'
    ]
    list_filter = ['tipo', 'unidade_crea', 'armario', 'prateleira', 'caixa', 'data_emissao', 'criado_em']
    search_fields = ['numero', 'cpf_cnpj', 'armario', 'prateleira', 'caixa', 'observacoes']
    readonly_fields = ['data_emissao', 'criado_em', 'atualizado_em', 'criado_por', 'identificador_local']
    date_hierarchy = 'data_emissao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'tipo', 'cpf_cnpj', 'unidade_crea')
        }),
        ('Local de Armazenamento', {
            'fields': ('armario', 'prateleira', 'caixa', 'identificador_local')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('SITAC', {
            'fields': ('protocolo_sitac',),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('criado_por', 'data_emissao', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se for uma nova criação
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
