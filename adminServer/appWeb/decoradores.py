from django.shortcuts import redirect
import datetime

#JABM (09-05/2020): Se agrega archivo de decoradores.py
from django.utils.decorators import method_decorator


def esta_logueado(vista):
    # JABM; Decorador que valida si esta logueado
    # Tomese como logueado que el usuario, pwd y token
    # estan correctos
    def interna(request):
        if not request.session.get('logueado', False):
            # JABM (09-05-2020): Si no esta logueado se redirigue al login.
            return redirect('/login/')
        # JABM (09-05-2020): Si esta logueado se permite acceso al recurso.
        return vista(request) 
    return interna

def esperando_token(vista):
    # JABM; Decorador que valida si esta esperando token
    # Tomese como esperando token un usuario que ya ingreso
    # su usuario y contraseña bien y esta en la página de solicitando_token
    def interna(request):
        if not request.session.get('token', False):
            # JABM (09-05-2020): Si no ha ingresado primero sus datos en login.
            return redirect('/login/')
        #JABM (09-05-2020): Si ya ha ingresado primero sus datos en login.
        return vista(request) 
    return interna

def no_esta_logueado(vista):
    #JABM; Decorador que valida si no se esta logueado
    #Tomese como logueado que el usuario, pwd y token
    #estan correctos
    def interna(request):
        if request.session.get('global', False):
            #JABM (09-05-2020): Si esta logueado como administrador global....
            return redirect('global:index')
        if request.session.get('logueado', False):
            #JABM (09-05-2020): Si esta logueado se redirigue a servidores.
            return redirect('/servidores/')
        #JABM (09-05-2020): Si no esta logueado se permite acceso al recurso.
        return vista(request) 
    return interna

def esta_logueado_global(vista):
    # MML; Decorador que valida si esta logueado
    # Tomese como logueado que el usuario, pwd y token
    # estan correctos
    def interna(request):
        if not request.session.get('global', False):
            # MML (05-07-2020): Si no esta logueado se redirigue al login.
            return redirect('login_global')
        # MML (05-07-2020): Si esta logueado se permite acceso al recurso.
        return vista(request) 
    return interna

def class_view_decorator(function_decorator):
    def deco(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View
    return deco