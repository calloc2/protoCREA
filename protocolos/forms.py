from django import forms
from .models import Protocolo
import re

class ProtocoloForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = [
            'numero', 'cpf_cnpj', 'unidade_crea', 'armario', 'prateleira', 'caixa', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número do protocolo'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'CPF (11 dígitos) ou CNPJ (14 dígitos)',
                'data-mask': 'cpf-cnpj'
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
            'cpf_cnpj': 'CPF/CNPJ',
            'unidade_crea': 'Unidade CREA-TO',
            'armario': 'Armário',
            'prateleira': 'Prateleira',
            'caixa': 'Caixa',
            'observacoes': 'Observações',
        }
        help_texts = {
            'numero': 'Número único do protocolo',
            'cpf_cnpj': 'CPF (11 dígitos) ou CNPJ (14 dígitos)',
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
        if cpf_cnpj:
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', cpf_cnpj)
            
            if len(cpf_cnpj_limpo) == 11:
                return cpf_cnpj_limpo
            elif len(cpf_cnpj_limpo) == 14:
                return cpf_cnpj_limpo
            else:
                raise forms.ValidationError(
                    'CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'
                )
        return cpf_cnpj

    def clean(self):
        """Validação geral do formulário"""
        cleaned_data = super().clean()
        cpf_cnpj = cleaned_data.get('cpf_cnpj')
        
        if cpf_cnpj:
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', cpf_cnpj)
            
            if len(cpf_cnpj_limpo) == 11:
                cleaned_data['tipo'] = 'profissional'
            elif len(cpf_cnpj_limpo) == 14:
                cleaned_data['tipo'] = 'empresa'
        
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
