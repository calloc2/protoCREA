from django.core.management.base import BaseCommand
from protocolos.models import TipoDocumento

class Command(BaseCommand):
    help = 'Popula os tipos de documentos no banco de dados'

    def handle(self, *args, **options):
        # Dados dos tipos de documentos por categoria
        tipos_documento_data = {
            'finalistico_pf': [
                'Anotação de Responsabilidade Técnica',
                'Atribuição Profissional',
                'Cancelamento de Registro',
                'Certidão de Acervo Técnico – CAT',
                'Certidão de Georreferenciamento',
                'Certidão de Registro e Quitação – CRQ',
                'Certidão Diversa',
                'Cobrança, Dívida Ativa e Financeiro',
                'Documento de Fiscalização',
                'Defesa de Fiscalização',
                'Denúncia',
                'Interrupção de Registro',
                'Recadastramento',
                'Reativação de Registro',
                'Registro',
                'Substituição de Registro Provisório para Definitivo',
                'Visto Profissional'
            ],
            'finalistico_pj': [
                'Atualização de Dados Cadastrais',
                'Baixa de Responsável Técnico',
                'Cadastro de Filial',
                'Cancelamento de Registro de Empresa',
                'Documento de Fiscalização',
                'Inclusão de Responsável Técnico',
                'Interrupção de Registro de Empresa',
                'Recadastramento',
                'Reativação de Registro',
                'Registro de instituição de Ensino',
                'Registro',
                'Visto de Empresa'
            ],
            'administrativo': [
                'Administrativos / Financeiro',
                'Aluguel',
                'Área de Patrimônio, Almoxarifado e Serviços Gerais',
                'Assessoria das Câmaras',
                'Assessoria de Comunicação',
                'Baixa de Pagamento de ART',
                'Cobrança / Dívida Ativa',
                'Colegiado',
                'Compra de Equipamento de Informática',
                'Compra de Material de Expediente / Limpeza',
                'Compra de Mobiliário',
                'Compra de Veículo',
                'Convênio',
                'Demonstrativo Financeiro',
                'Diárias, Passagens, Deslocamentos, Ajuda de Custo',
                'Eleição',
                'Gerência de ART e Gerência Técnica',
                'Gerência de Fiscalização',
                'Gerência de Tecnologia da Informação',
                'Honorários',
                'Infraestrutura',
                'Licitação',
                'Memorando',
                'Ofício',
                'Outros',
                'Ouvidoria',
                'Passagem Aérea',
                'Plenário',
                'Presidência',
                'Protocolo',
                'Renovação de Contrato',
                'Ressarcimento',
                'Seguro',
                'Superintendência',
                'Suprimento de Fundos',
                'Transporte'
            ]
        }

        # Limpar tipos existentes
        TipoDocumento.objects.all().delete()
        self.stdout.write('Tipos de documentos existentes removidos.')

        # Criar novos tipos
        total_criados = 0
        for categoria, tipos in tipos_documento_data.items():
            for tipo_nome in tipos:
                TipoDocumento.objects.create(
                    categoria=categoria,
                    nome=tipo_nome,
                    ativo=True
                )
                total_criados += 1

        self.stdout.write(
            self.style.SUCCESS(f'Criados {total_criados} tipos de documentos com sucesso!')
        )
