from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("editar-perfil/", views.editar_perfil, name="editar_perfil"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
