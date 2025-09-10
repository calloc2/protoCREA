from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Protocolo, LocalArmazenamento, TipoDocumento, Documento
from .forms import ProtocoloForm

def protocolo_list(request):
    """Lista todos os protocolos com filtros e paginação"""
    q = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "")
    unidade_crea = request.GET.get("unidade_crea", "")
    armario = request.GET.get("armario", "").strip()
    prateleira = request.GET.get("prateleira", "").strip()
    caixa = request.GET.get("caixa", "").strip()
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")
    itens_por_pagina = request.GET.get("itens_por_pagina", "10")
    
    try:
        itens_por_pagina = int(itens_por_pagina)
        if itens_por_pagina not in [10, 50, 100]:
            itens_por_pagina = 10
    except ValueError:
        itens_por_pagina = 10
    
    qs = Protocolo.objects.all()
    
    if q:
        qs = qs.filter(
            Q(numero__icontains=q) |
            Q(cpf_cnpj__icontains=q) |
            Q(armario__icontains=q) |
            Q(prateleira__icontains=q) |
            Q(caixa__icontains=q) |
            Q(observacoes__icontains=q)
        )
    
    if tipo:
        qs = qs.filter(tipo=tipo)
    
    if unidade_crea:
        qs = qs.filter(unidade_crea=unidade_crea)
    
    if armario:
        qs = qs.filter(armario=armario)
    
    if prateleira:
        qs = qs.filter(prateleira=prateleira)
    
    if caixa:
        qs = qs.filter(caixa=caixa)
    
    if data_inicio:
        try:
            data_inicio_parsed = parse_date(data_inicio)
            if data_inicio_parsed:
                qs = qs.filter(data_emissao__gte=data_inicio_parsed)
        except (ValueError, TypeError):
            pass
    
    if data_fim:
        try:
            data_fim_parsed = parse_date(data_fim)
            if data_fim_parsed:
                qs = qs.filter(data_emissao__lte=data_fim_parsed)
        except (ValueError, TypeError):
            pass
    
    paginator = Paginator(qs, itens_por_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "q": q,
        "tipo": tipo,
        "unidade_crea": unidade_crea,
        "armario": armario,
        "prateleira": prateleira,
        "caixa": caixa,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "itens_por_pagina": itens_por_pagina,
        "tipos": Protocolo.TIPO_CHOICES,
        "unidades_crea": Protocolo.UNIDADE_CHOICES,
        "opcoes_paginacao": [10, 50, 100],
        "user_can_edit": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_edit,
        "user_can_publish": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_publish,
    }
    return render(request, "protocolos/lista.html", context)

def protocolo_detail(request, pk):
    """Visualiza detalhes de um protocolo específico"""
    protocolo = get_object_or_404(Protocolo, pk=pk)
    

    
    context = {
        "protocolo": protocolo,
        "user_can_edit": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_edit,
        "user_can_publish": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_publish,
    }
    return render(request, "protocolos/detalhe.html", context)

@login_required
def protocolo_create(request):
    """View para criar novo protocolo"""
    if not hasattr(request.user, 'perfil') or not request.user.perfil.can_publish:
        messages.error(request, 'Você não tem permissão para criar protocolos.')
        return redirect('protocolos:lista')
    
    if request.method == 'POST':
        form = ProtocoloForm(request.POST, user=request.user)
        if form.is_valid():
            protocolo = form.save(commit=False)
            protocolo.criado_por = request.user
            protocolo.save()
            
            # Processar documentos enviados via JavaScript
            documentos_data = {}
            for key, value in request.POST.items():
                if key.startswith('documentos[') and ']' in key:
                    # Extrair índice e campo do formato: documentos[0][tipo_documento]
                    parts = key.split('[')
                    if len(parts) >= 3:
                        index = parts[1].rstrip(']')
                        field = parts[2].rstrip(']')
                        
                        if index not in documentos_data:
                            documentos_data[index] = {}
                        documentos_data[index][field] = value
            
            # Criar documentos
            documentos_criados = 0
            for doc_data in documentos_data.values():
                if doc_data.get('tipo_documento'):
                    try:
                        tipo_doc = TipoDocumento.objects.get(id=doc_data['tipo_documento'])
                        Documento.objects.create(
                            protocolo=protocolo,
                            tipo_documento=tipo_doc,
                            observacoes=doc_data.get('observacoes', '')
                        )
                        documentos_criados += 1
                    except TipoDocumento.DoesNotExist:
                        pass
            
            if documentos_criados > 0:
                messages.success(request, f'Protocolo criado com sucesso! {documentos_criados} documento(s) adicionado(s).')
            else:
                messages.success(request, 'Protocolo criado com sucesso!')
            return redirect('protocolos:detalhe', pk=protocolo.pk)
    else:
        form = ProtocoloForm(user=request.user)
    
    context = {
        'form': form,
        'action': 'criar',
        'title': 'Criar Novo Protocolo'
    }
    return render(request, 'protocolos/form.html', context)

@login_required
def protocolo_edit(request, pk):
    """View para editar protocolo existente"""
    protocolo = get_object_or_404(Protocolo, pk=pk)
    
    if not hasattr(request.user, 'perfil'):
        messages.error(request, 'Perfil não encontrado.')
        return redirect('protocolos:lista')
    
    perfil = request.user.perfil
    
    if not (perfil.can_edit or protocolo.criado_por == request.user):
        messages.error(request, 'Você não tem permissão para editar este protocolo.')
        return redirect('protocolos:detalhe', pk=protocolo.pk)
    
    if request.method == 'POST':
        form = ProtocoloForm(request.POST, instance=protocolo, user=request.user)
        if form.is_valid():
            protocolo = form.save()
            messages.success(request, 'Protocolo atualizado com sucesso!')
            return redirect('protocolos:detalhe', pk=protocolo.pk)
    else:
        form = ProtocoloForm(instance=protocolo, user=request.user)
    
    context = {
        'form': form,
        'protocolo': protocolo,
        'action': 'editar',
        'title': 'Editar Protocolo'
    }
    return render(request, 'protocolos/form.html', context)

@login_required
def protocolo_delete(request, pk):
    """View para deletar protocolo"""
    protocolo = get_object_or_404(Protocolo, pk=pk)
    
    if not hasattr(request.user, 'perfil'):
        messages.error(request, 'Perfil não encontrado.')
        return redirect('protocolos:lista')
    
    perfil = request.user.perfil
    
    if not (perfil.can_edit or protocolo.criado_por == request.user):
        messages.error(request, 'Você não tem permissão para excluir este protocolo.')
        return redirect('protocolos:detalhe', pk=protocolo.pk)
    
    if request.method == 'POST':
        numero_protocolo = protocolo.numero
        protocolo.delete()
        messages.success(request, f'Protocolo {numero_protocolo} excluído com sucesso!')
        return redirect('protocolos:lista')
    
    # Se não for POST, redireciona para a lista
    return redirect('protocolos:lista')

def tipos_documento_api(request):
    """API para buscar tipos de documento por categoria"""
    categoria = request.GET.get('categoria', '')
    
    if not categoria:
        return JsonResponse({'tipos': []})
    
    tipos = TipoDocumento.objects.filter(
        categoria=categoria,
        ativo=True
    ).order_by('nome')
    
    tipos_data = [
        {
            'id': tipo.id,
            'nome': tipo.nome
        }
        for tipo in tipos
    ]
    
    return JsonResponse({'tipos': tipos_data})