from django.urls import path
from . import views

app_name = "protocolos"

urlpatterns = [
    path("", views.protocolo_list, name="lista"),
    path("protocolo/<int:pk>/", views.protocolo_detail, name="detalhe"),
    path("protocolo/criar/", views.protocolo_create, name="criar"),
    path("protocolo/<int:pk>/editar/", views.protocolo_edit, name="editar"),
    path("protocolo/<int:pk>/deletar/", views.protocolo_delete, name="deletar"),
    path("tipos-documento/", views.tipos_documento_api, name="tipos_documento_api"),
]
