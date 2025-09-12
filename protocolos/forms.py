from django import forms
from .models import Protocolo, TipoDocumento, Documento
from django.conf import settings
import re


def _validate_cpf(cpf: str) -> bool:
    # Remove non-digits
    cpf = re.sub(r"\D", "", cpf or "")
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    # First digit
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (sum1 * 10) % 11
    d1 = 0 if d1 == 10 else d1
    # Second digit
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (sum2 * 10) % 11
    d2 = 0 if d2 == 10 else d2
    return int(cpf[9]) == d1 and int(cpf[10]) == d2


def _validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r"\D", "", cnpj or "")
    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    d1 = 11 - (sum1 % 11)
    d1 = 0 if d1 >= 10 else d1
    weights2 = [6] + weights1
    sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    d2 = 11 - (sum2 % 11)
    d2 = 0 if d2 >= 10 else d2
    return int(cnpj[12]) == d1 and int(cnpj[13]) == d2

class ProtocoloForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = [
            'numero', 'tipo', 'cpf_cnpj', 'unidade_crea', 'armario', 'prateleira', 'caixa', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número do protocolo'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_tipo'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'CPF (11 dígitos) ou CNPJ (14 dígitos)',
                'data-mask': 'cpf-cnpj',
                'id': 'id_cpf_cnpj'
            }),
            'unidade_crea': forms.Select(attrs={'class': 'form-control'}),
            'armario': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: 1, 2, 3...',
                'pattern': '[0-9]+', 'title': 'Apenas números são permitidos'
            }),
            'prateleira': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: 1, 2, 3...',
                'pattern': '[0-9]+', 'title': 'Apenas números são permitidos'
            }),
            'caixa': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: 1, 2, 3...',
                'pattern': '[0-9]+', 'title': 'Apenas números são permitidos'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais'
            }),
        }
        labels = {
            'numero': 'Número de Protocolo',
            'tipo': 'Tipo de Processo',
            'cpf_cnpj': 'CPF/CNPJ',
            'unidade_crea': 'Unidade CREA-TO',
            'armario': 'Armário',
            'prateleira': 'Prateleira',
            'caixa': 'Caixa',
            'observacoes': 'Observações',
        }
        help_texts = {
            'numero': 'Número único do protocolo',
            'tipo': 'Selecione o tipo de processo',
            'cpf_cnpj': 'CPF (11 dígitos) ou CNPJ (14 dígitos) - obrigatório para processos finalísticos',
            'unidade_crea': 'Unidade do CREA-TO responsável pelo protocolo',
            'armario': 'Número do armário (apenas números)',
            'prateleira': 'Número da prateleira (apenas números)',
            'caixa': 'Número da caixa (apenas números)',
            'observacoes': 'Observações adicionais sobre o protocolo',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and hasattr(self.user, 'perfil') and not self.instance.pk:
            self.fields['unidade_crea'].initial = self.user.perfil.local
        for field_name, field in self.fields.items():
            if hasattr(field, 'label'):
                field.label = field.label

    def clean_cpf_cnpj(self):
        """Validação e formatação do CPF/CNPJ"""
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        tipo = self.cleaned_data.get('tipo')
        
        # Para processos administrativos, CPF/CNPJ não deve ser informado
        if tipo == 'administrativo' and cpf_cnpj:
            raise forms.ValidationError(
                'CPF/CNPJ não deve ser informado para processos administrativos'
            )
        
        # Para processos finalísticos, CPF/CNPJ é obrigatório
        if tipo in ['finalistico_pf', 'finalistico_pj'] and not cpf_cnpj:
            raise forms.ValidationError(
                'CPF/CNPJ é obrigatório para processos finalísticos'
            )
        
        if cpf_cnpj:
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', cpf_cnpj)
            
            # Validação específica por tipo com dígitos verificadores
            if tipo == 'finalistico_pf':
                if len(cpf_cnpj_limpo) != 11:
                    raise forms.ValidationError('CPF deve ter 11 dígitos.')
                if settings.STRICT_CPF_CNPJ and not _validate_cpf(cpf_cnpj_limpo):
                    raise forms.ValidationError('CPF inválido.')
            elif tipo == 'finalistico_pj':
                if len(cpf_cnpj_limpo) != 14:
                    raise forms.ValidationError('CNPJ deve ter 14 dígitos.')
                if settings.STRICT_CPF_CNPJ and not _validate_cnpj(cpf_cnpj_limpo):
                    raise forms.ValidationError('CNPJ inválido.')
            
            return cpf_cnpj_limpo
        return cpf_cnpj

    def clean(self):
        """Validação geral do formulário"""
        cleaned_data = super().clean()
        return cleaned_data

    def clean_armario(self):
        armario = self.cleaned_data.get('armario')
        if armario and not armario.isdigit():
            raise forms.ValidationError('O armário deve conter apenas números.')
        return armario

    def clean_prateleira(self):
        prateleira = self.cleaned_data.get('prateleira')
        if prateleira and not prateleira.isdigit():
            raise forms.ValidationError('A prateleira deve conter apenas números.')
        return prateleira

    def clean_caixa(self):
        caixa = self.cleaned_data.get('caixa')
        if caixa and not caixa.isdigit():
            raise forms.ValidationError('A caixa deve conter apenas números.')
        return caixa

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'observacoes']
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações sobre este documento'
            }),
        }
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'observacoes': 'Observações',
        }

    def __init__(self, *args, **kwargs):
        tipo_processo = kwargs.pop('tipo_processo', None)
        super().__init__(*args, **kwargs)
        
        if tipo_processo:
            # Filtra os tipos de documento baseado no tipo do processo
            self.fields['tipo_documento'].queryset = TipoDocumento.objects.filter(
                categoria=tipo_processo,
                ativo=True
            ).order_by('nome')
