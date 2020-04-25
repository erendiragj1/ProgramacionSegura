from django.shortcuts import render
from django.contrib import admin
from django.urls import path
# Create your views here.
from appMain.sites import *

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', login),
    path('login/', login),
    path('servidores/', servidores),
    path('usuarios/', usuarios),
    path('logout/', logout),
    path('actualizaSrv/',actualizaSrv),
    path('actualizaStatus/',actualizaStatus),
]