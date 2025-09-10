from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from usuarios.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Atribui usuários aos grupos baseado em suas permissões no perfil'

    def handle(self, *args, **options):
        # Mapeamento de permissões para grupos
        permissao_grupo_map = {
            'visualizador': 'Visualizadores',
            'editor': 'Editores', 
            'publicador': 'Publicadores',
            'admin': 'Administradores'
        }

        usuarios_atualizados = 0
        
        for perfil in PerfilUsuario.objects.all():
            if perfil.conta_aprovada:  # Só atribui grupos para usuários aprovados
                grupo_nome = permissao_grupo_map.get(perfil.permissao)
                
                if grupo_nome:
                    try:
                        grupo = Group.objects.get(name=grupo_nome)
                        
                        # Remove o usuário de todos os grupos primeiro
                        perfil.user.groups.clear()
                        
                        # Adiciona ao grupo correspondente
                        perfil.user.groups.add(grupo)
                        
                        self.stdout.write(
                            f'✅ {perfil.user.get_full_name()} ({perfil.user.username}) → {grupo_nome}'
                        )
                        usuarios_atualizados += 1
                        
                    except Group.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Grupo "{grupo_nome}" não encontrado')
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Permissão "{perfil.permissao}" não mapeada para {perfil.user.username}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Usuário {perfil.user.username} não aprovado, pulando...')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 {usuarios_atualizados} usuários atribuídos aos grupos com sucesso!')
        )
