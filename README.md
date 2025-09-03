# Protocolos CREA-TO

Sistema de gerenciamento de protocolos do CREA-TO.
<img width="1813" height="785" alt="image" src="https://github.com/user-attachments/assets/55c1becd-c369-4ae4-ab16-8366cc56d85c" />


## Estrutura do Projeto

```
normativosCREA/
├── core/                   # Configurações principais do Django
├── protocolos/             # Aplicação principal
├── usuarios/               # Sistema de usuários e perfis
├── media/                  # Arquivos de upload (PDFs, anexos)
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   └── images/             # Imagens (logo CREA-TO)
├── templates/              # Templates HTML
└── manage.py               # Script de gerenciamento Django
```

## Configuração de Arquivos

### Arquivos Estáticos (`static/`)
- **Logo e imagens**: `static/images/`
- **CSS e JavaScript**: `static/`
- **Configuração**: `STATIC_URL = 'static/'` e `STATICFILES_DIRS`

### Arquivos de Mídia (`media/`)
- **PDFs dos protocolos**: `media/protocolos/`
- **Configuração**: `MEDIA_URL = '/media/'` e `MEDIA_ROOT`
- **Gitignore**: A pasta `media/` está no `.gitignore` para não versionar arquivos de upload

### Funcionalidades Implementadas
- **Gerenciamento de protocolos**: Criação, edição e visualização
- **Sistema de usuários**: Cadastro, login e perfis
- **Controle de acesso**: Diferentes níveis de permissão
- **Busca e filtros**: Por número, assunto, unidade CREA
- **Status de protocolos**: Ativo, arquivado, etc.

## Desenvolvimento

### Instalação
1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente no arquivo `.env`
6. Execute as migrações: `python manage.py migrate`
7. Inicie o servidor: `python manage.py runserver`

### Estrutura de Upload
- Os PDFs são salvos automaticamente em `media/protocolos/`
- Em desenvolvimento, os arquivos são servidos via `MEDIA_URL`

## Tecnologias
- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5.3
- **Banco de Dados**: PostgreSQL
