from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from protocolos.models import Protocolo, TipoDocumento, Documento
from usuarios.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Cria os grupos de usuários e suas permissões'

    def handle(self, *args, **options):
        # Definir os grupos e suas permissões
        grupos_config = {
            'Visualizadores': {
                'description': 'Usuários que podem apenas visualizar protocolos',
                'permissions': [
                    ('protocolos', 'view_protocolo'),
                    ('protocolos', 'view_tipodocumento'),
                    ('protocolos', 'view_documento'),
                    ('usuarios', 'view_perfilusuario'),
                ]
            },
            'Editores': {
                'description': 'Usuários que podem criar e editar protocolos',
                'permissions': [
                    ('protocolos', 'view_protocolo'),
                    ('protocolos', 'add_protocolo'),
                    ('protocolos', 'change_protocolo'),
                    ('protocolos', 'view_tipodocumento'),
                    ('protocolos', 'view_documento'),
                    ('protocolos', 'add_documento'),
                    ('protocolos', 'change_documento'),
                    ('usuarios', 'view_perfilusuario'),
                ]
            },
            'Publicadores': {
                'description': 'Usuários que podem publicar e gerenciar protocolos',
                'permissions': [
                    ('protocolos', 'view_protocolo'),
                    ('protocolos', 'add_protocolo'),
                    ('protocolos', 'change_protocolo'),
                    ('protocolos', 'delete_protocolo'),
                    ('protocolos', 'view_tipodocumento'),
                    ('protocolos', 'add_tipodocumento'),
                    ('protocolos', 'change_tipodocumento'),
                    ('protocolos', 'view_documento'),
                    ('protocolos', 'add_documento'),
                    ('protocolos', 'change_documento'),
                    ('protocolos', 'delete_documento'),
                    ('usuarios', 'view_perfilusuario'),
                    ('usuarios', 'change_perfilusuario'),
                ]
            },
            'Administradores': {
                'description': 'Usuários com acesso total ao sistema',
                'permissions': [
                    # Todas as permissões de protocolos
                    ('protocolos', 'view_protocolo'),
                    ('protocolos', 'add_protocolo'),
                    ('protocolos', 'change_protocolo'),
                    ('protocolos', 'delete_protocolo'),
                    ('protocolos', 'view_tipodocumento'),
                    ('protocolos', 'add_tipodocumento'),
                    ('protocolos', 'change_tipodocumento'),
                    ('protocolos', 'delete_tipodocumento'),
                    ('protocolos', 'view_documento'),
                    ('protocolos', 'add_documento'),
                    ('protocolos', 'change_documento'),
                    ('protocolos', 'delete_documento'),
                    # Todas as permissões de usuários
                    ('usuarios', 'view_perfilusuario'),
                    ('usuarios', 'add_perfilusuario'),
                    ('usuarios', 'change_perfilusuario'),
                    ('usuarios', 'delete_perfilusuario'),
                    # Permissões de autenticação
                    ('auth', 'view_user'),
                    ('auth', 'add_user'),
                    ('auth', 'change_user'),
                    ('auth', 'delete_user'),
                    ('auth', 'view_group'),
                    ('auth', 'add_group'),
                    ('auth', 'change_group'),
                    ('auth', 'delete_group'),
                ]
            }
        }

        # Criar ou atualizar grupos
        for nome_grupo, config in grupos_config.items():
            grupo, created = Group.objects.get_or_create(name=nome_grupo)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Grupo "{nome_grupo}" criado com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Grupo "{nome_grupo}" já existe, atualizando permissões...')
                )
            
            # Limpar permissões existentes
            grupo.permissions.clear()
            
            # Adicionar novas permissões
            permissoes_adicionadas = 0
            for app_label, codename in config['permissions']:
                try:
                    permission = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    grupo.permissions.add(permission)
                    permissoes_adicionadas += 1
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Permissão não encontrada: {app_label}.{codename}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'   📋 {permissoes_adicionadas} permissões adicionadas ao grupo "{nome_grupo}"')
            )

        # Criar perfil para o usuário admin se não existir
        try:
            from django.contrib.auth.models import User
            admin_user = User.objects.get(username='admin')
            if not hasattr(admin_user, 'perfil'):
                PerfilUsuario.objects.create(
                    user=admin_user,
                    cpf='000.000.000-00',
                    permissao='admin',
                    pode_publicar=True,
                    conta_aprovada=True,
                    local='sede_palmas'
                )
                self.stdout.write(
                    self.style.SUCCESS('✅ Perfil criado para o usuário admin')
                )
            
            # Adicionar admin ao grupo de administradores
            admin_group = Group.objects.get(name='Administradores')
            admin_user.groups.add(admin_group)
            self.stdout.write(
                self.style.SUCCESS('✅ Usuário admin adicionado ao grupo Administradores')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('⚠️ Usuário admin não encontrado')
            )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Grupos de usuários criados com sucesso!')
        )
        self.stdout.write('\n📋 Grupos disponíveis:')
        for grupo in Group.objects.all():
            self.stdout.write(f'   • {grupo.name} ({grupo.permissions.count()} permissões)')
