from django import forms
from .models import Protocolo, TipoDocumento, Documento
import re

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
            
            # Validação específica por tipo
            if tipo == 'finalistico_pf' and len(cpf_cnpj_limpo) != 11:
                raise forms.ValidationError(
                    'CPF deve ter 11 dígitos para processos finalísticos de pessoa física'
                )
            elif tipo == 'finalistico_pj' and len(cpf_cnpj_limpo) != 14:
                raise forms.ValidationError(
                    'CNPJ deve ter 14 dígitos para processos finalísticos de pessoa jurídica'
                )
            
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
