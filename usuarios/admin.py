from django.contrib import admin
from django.contrib.auth.models import User
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'cpf', 'permissao',
        'conta_aprovada', 'pode_publicar', 'criado_em'
    ]
    list_filter = [
        'permissao', 'conta_aprovada',
        'pode_publicar', 'criado_em', 'data_aprovacao'
    ]
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'cpf']
    ordering = ['-criado_em']

    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'telefone')
        }),
        ('Informações Profissionais', {
            'fields': ('registro_profissional', 'empresa', 'cargo')
        }),
        ('Permissões', {
            'fields': ('permissao', 'pode_publicar'),
            'description': 'Configure as permissões do usuário'
        }),
        ('Status da Conta', {
            'fields': ('conta_aprovada', 'data_aprovacao', 'aprovado_por'),
            'classes': ('collapse',),
            'description': 'Controle de aprovação da conta'
        }),
        ('Datas Importantes', {
            'fields': ('criado_em', 'atualizado_em', 'ultimo_acesso'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['criado_em', 'atualizado_em']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'aprovado_por')

    actions = [
        'aprovar_usuarios', 'rejeitar_usuarios', 
        'permitir_publicar_atas', 'revogar_publicar_atas',
        'promover_para_admin', 'promover_para_publicador', 'promover_para_editor'
    ]

    def aprovar_usuarios(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            conta_aprovada=True,
            data_aprovacao=timezone.now(),
            aprovado_por=request.user
        )
        self.message_user(request, f'{updated} perfil(is) de usuário(s) aprovado(s) com sucesso.')
    aprovar_usuarios.short_description = "✅ Aprovar contas selecionadas"

    def rejeitar_usuarios(self, request, queryset):
        updated = queryset.update(conta_aprovada=False, data_aprovacao=None, aprovado_por=None)
        self.message_user(request, f'{updated} perfil(is) de usuário(s) rejeitado(s).')
    rejeitar_usuarios.short_description = "❌ Rejeitar contas selecionadas"

    def permitir_publicar_atas(self, request, queryset):
        updated = queryset.update(pode_publicar=True)
        self.message_user(request, f'{updated} usuário(s) agora podem publicar atas.')
    permitir_publicar_atas.short_description = "📝 Permitir publicar atas"

    def revogar_publicar_atas(self, request, queryset):
        updated = queryset.update(pode_publicar=False)
        self.message_user(request, f'{updated} usuário(s) não podem mais publicar atas.')
    revogar_publicar_atas.short_description = "🚫 Revogar permissão de publicar atas"

    def promover_para_admin(self, request, queryset):
        updated = queryset.update(permissao='admin', pode_publicar=True)
        self.message_user(request, f'{updated} usuário(s) promovido(s) para Administrador.')
    promover_para_admin.short_description = "👑 Promover para Administrador"

    def promover_para_publicador(self, request, queryset):
        updated = queryset.update(permissao='publicador', pode_publicar=True)
        self.message_user(request, f'{updated} usuário(s) promovido(s) para Publicador.')
    promover_para_publicador.short_description = "📝 Promover para Publicador"

    def promover_para_editor(self, request, queryset):
        updated = queryset.update(permissao='editor')
        self.message_user(request, f'{updated} usuário(s) promovido(s) para Editor.')
    promover_para_editor.short_description = "✏️ Promover para Editor"
