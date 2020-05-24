from django.shortcuts import redirect
import datetime

#JABM (09-05/2020): Se agrega archivo de decoradores.py

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
        # JABM (09-05-2020): Si ya ha ingresado primero sus datos en login.
        return vista(request) 
    return interna