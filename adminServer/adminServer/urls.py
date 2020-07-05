"""adminServer URL Configuration

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
from django.urls import path, include
from appWeb.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login,name='login'),
    path('accounts/login/',login_global,name='login_global'),
    path('global/', include(('appWeb.urls','global'))),
    path('token_global/', solicitar_token_global, name="token_global"),
    path('',login),
    path('esperar_token/', solicitar_token, name="solicitar_token"),
    path('servidores/',servidores, name="servidores"),
    path('logout/',logout,name="logout"),
    path('monitor/<str:pk>/',monitoreo,name="monitor"),
    path('monitoreo_ajax/<str:pk>/',monitoreo_ajax,name="monitoreo_ajax"),
]
