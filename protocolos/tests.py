from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Protocolo

User = get_user_model()

class ProtocoloModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_criar_protocolo_profissional(self):
        """Testa criação de protocolo para profissional (CPF)"""
        protocolo = Protocolo.objects.create(
            numero='PROT001',
            cpf_cnpj='12345678901',
            local_armazenamento='CAIXA A, FILEIRA 1, FACE 1',
            criado_por=self.user
        )
        
        self.assertEqual(protocolo.tipo, 'profissional')
        self.assertEqual(protocolo.cpf_cnpj_formatado, '123.456.789-01')
        self.assertIsNone(protocolo.protocolo_sitac)
    
    def test_criar_protocolo_empresa(self):
        """Testa criação de protocolo para empresa (CNPJ)"""
        protocolo = Protocolo.objects.create(
            numero='PROT002',
            cpf_cnpj='12345678000195',
            local_armazenamento='CAIXA B, FILEIRA 2, FACE 1',
            criado_por=self.user
        )
        
        self.assertEqual(protocolo.tipo, 'empresa')
        self.assertEqual(protocolo.cpf_cnpj_formatado, '12.345.678/0001-95')
        self.assertIsNone(protocolo.protocolo_sitac)
    
    def test_cpf_cnpj_invalido(self):
        """Testa validação de CPF/CNPJ inválido"""
        with self.assertRaises(ValidationError):
            protocolo = Protocolo(
                numero='PROT003',
                cpf_cnpj='123456789',  # Número inválido
                local_armazenamento='CAIXA C, FILEIRA 3, FACE 1',
                criado_por=self.user
            )
            protocolo.full_clean()
    
    def test_numero_unico(self):
        """Testa que número de protocolo deve ser único"""
        Protocolo.objects.create(
            numero='PROT004',
            cpf_cnpj='12345678901',
            local_armazenamento='CAIXA D, FILEIRA 4, FACE 1',
            criado_por=self.user
        )
        
        with self.assertRaises(Exception):  # IntegrityError ou similar
            Protocolo.objects.create(
                numero='PROT004',  # Mesmo número
                cpf_cnpj='98765432109',
                local_armazenamento='CAIXA E, FILEIRA 5, FACE 1',
                criado_por=self.user
            )
    
    def test_str_representation(self):
        """Testa representação string do modelo"""
        protocolo = Protocolo.objects.create(
            numero='PROT005',
            cpf_cnpj='12345678901',
            local_armazenamento='CAIXA F, FILEIRA 6, FACE 1',
            criado_por=self.user
        )
        
        expected = f"Protocolo {protocolo.numero} - {protocolo.get_tipo_display()}"
        self.assertEqual(str(protocolo), expected)
    
    def test_ordering(self):
        """Testa ordenação dos protocolos"""
        # Criar protocolos em ordem diferente
        protocolo1 = Protocolo.objects.create(
            numero='PROT006',
            cpf_cnpj='12345678901',
            local_armazenamento='CAIXA G, FILEIRA 7, FACE 1',
            criado_por=self.user
        )
        
        protocolo2 = Protocolo.objects.create(
            numero='PROT007',
            cpf_cnpj='98765432109',
            local_armazenamento='CAIXA H, FILEIRA 8, FACE 1',
            criado_por=self.user
        )
        
        protocolos = Protocolo.objects.all()
        self.assertEqual(protocolos[0], protocolo2)  # Mais recente primeiro
        self.assertEqual(protocolos[1], protocolo1)
