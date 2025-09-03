# Módulo de Protocolos

Este módulo permite o cadastro e gerenciamento de protocolos no sistema CREA-TO.

## Funcionalidades

- **Cadastro de Protocolos**: Criação de novos protocolos com validação automática
- **Listagem com Filtros**: Busca por número, CPF/CNPJ, tipo e data
- **Validação Automática**: Tipo (Profissional/Empresa) determinado pelo número de dígitos
- **Formatação Automática**: CPF/CNPJ formatado automaticamente
- **Controle de Acesso**: Baseado no perfil do usuário

## Campos do Modelo

### Protocolo
- **numero**: Número único do protocolo (obrigatório)
- **data_emissao**: Data de criação (automática)
- **cpf_cnpj**: CPF (11 dígitos) ou CNPJ (14 dígitos)
- **tipo**: Profissional ou Empresa (determinado automaticamente)
- **local_armazenamento**: Local onde o processo está armazenado
- **observacoes**: Observações adicionais (opcional)
- **protocolo_sitac**: Número de protocolo retornado pela API do SITAC
- **criado_por**: Usuário que criou o protocolo
- **criado_em**: Data/hora de criação
- **atualizado_em**: Data/hora da última atualização

## Validações

- CPF deve ter exatamente 11 dígitos
- CNPJ deve ter exatamente 14 dígitos
- Número de protocolo deve ser único
- Tipo é determinado automaticamente pelo número de dígitos
- Campo protocolo_sitac é preenchido automaticamente pela API do SITAC

## URLs

- `/protocolos/` - Lista de protocolos
- `/protocolos/protocolo/<id>/` - Detalhes do protocolo
- `/protocolos/protocolo/criar/` - Criar novo protocolo
- `/protocolos/protocolo/<id>/editar/` - Editar protocolo

## Permissões

- **Visualizar**: Todos os usuários autenticados
- **Criar**: Usuários com `can_publish`
- **Editar**: Usuários com `can_edit` ou criador do protocolo

## Formatação Automática

### CPF
- Entrada: `12345678901`
- Saída: `123.456.789-01`

### CNPJ
- Entrada: `12345678000195`
- Saída: `12.345.678/0001-95`

## Exemplos de Uso

### Criar Protocolo para Profissional
```python
protocolo = Protocolo.objects.create(
    numero='PROT001',
    cpf_cnpj='12345678901',  # CPF com 11 dígitos
    local_armazenamento='CAIXA A, FILEIRA 1, FACE 1',
    criado_por=usuario
)
# Tipo será automaticamente definido como 'profissional'
```

### Criar Protocolo para Empresa
```python
protocolo = Protocolo.objects.create(
    numero='PROT002',
    cpf_cnpj='12345678000195',  # CNPJ com 14 dígitos
    local_armazenamento='CAIXA B, FILEIRA 2, FACE 1',
    criado_por=usuario
)
# Tipo será automaticamente definido como 'empresa'
```

## Testes

Execute os testes com:
```bash
python manage.py test protocolos
```

## Admin

O modelo está configurado no Django Admin com:
- Lista com filtros por tipo e data
- Busca por número, CPF/CNPJ e local
- Campo SITAC em seção colapsável
- Campos de controle em seção colapsável
- Hierarquia por data de emissão
