#!/usr/bin/env python
"""
Script para popular os tipos de documentos no banco de dados
Execute com: python manage.py shell < protocolos/fixtures/popular_tipos_documento.py
"""

from protocolos.models import TipoDocumento

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

# Criar novos tipos
for categoria, tipos in tipos_documento_data.items():
    for tipo_nome in tipos:
        TipoDocumento.objects.create(
            categoria=categoria,
            nome=tipo_nome,
            ativo=True
        )

print(f"Criados {TipoDocumento.objects.count()} tipos de documentos")
