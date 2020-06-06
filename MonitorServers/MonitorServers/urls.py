"""MonitorServers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from appMonitoreo.views import *  # NOQA
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('datos_monitor/',listar_datos, name='listar_datos'),
    path('authenticacion/',views.obtain_auth_token),
]

# curl http://localhost:8000/authentication/user = miguel/ pass = hola