from django.urls import path
from .views import *

urlpatterns = [
    path('',Inicio.as_view(),name='index'),
    path('crear_admin/',CrearAdministrador.as_view(),name='crear_admin'),
    path('listar_admin/',ListarAdministrador.as_view(), name = 'listar_admin'),
    path('editar_admin/<str:pk>/',ActualizarAdministrador.as_view(), name = 'editar_admin'),
    path('eliminar_admin/<str:pk>/',EliminarAdministrador.as_view(), name = 'eliminar_admin'),

    path('listar_server/',ListarServidor.as_view() , name = 'listar_server'),
    path('crear_server/',CrearServer.as_view(), name = 'crear_server'),
    path('editar_server/<int:pk>/',ActualizarServidor.as_view() , name = 'editar_server'),
    path('eliminar_server/<int:pk>/', EliminarServidor.as_view(), name = 'eliminar_server')
]
