from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(Inicio),name='index'),
    path('logout/',login_required(logoutAdmin),name="logout_global"),
    path('crear_admin/',login_required(CrearAdministrador.as_view()),name='crear_admin'),
    path('listar_admin/',login_required(ListarAdministrador.as_view()), name = 'listar_admin'),
    path('editar_admin/<str:pk>/',login_required(ActualizarAdministrador.as_view()), name = 'editar_admin'),
    path('eliminar_admin/<str:pk>/',login_required(EliminarAdministrador.as_view()), name = 'eliminar_admin'),

    path('listar_server/',login_required(ListarServidor.as_view()), name = 'listar_server'),
    path('crear_server/',login_required(CrearServer.as_view()), name = 'crear_server'),
    path('editar_server/<int:pk>/',login_required(ActualizarServidor.as_view()) , name = 'editar_server'),
    path('eliminar_server/<int:pk>/',login_required(EliminarServidor.as_view()), name = 'eliminar_server')
]
