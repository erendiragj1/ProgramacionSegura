from django.contrib.auth import authenticate,login as do_login,logout as do_logout
from django.http import HttpResponseRedirect
from django.contrib.auth import signals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import *
from .models import *
import requests
from . import api
from appWeb import decoradores
from axes.decorators import axes_dispatch
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView
import json
import logging
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import response
from json_response import JsonResponse
# Create your views here.
from django.conf import settings


#PATH_LOG: Se define en el archivo de settings.py
logging.basicConfig(filename=settings.PATH_LOG, format='%(asctime)s %(message)s', level=logging.DEBUG)

@axes_dispatch
@decoradores.no_esta_logueado
def login(request):
    logging.info('login: Se hace petición por el método: ' + request.method)
    user_form = userForm()
    if request.method == "POST":
        nomUsuario = request.POST.get("usr")
        pwdEnviada = request.POST.get("pwd")
        # MML se usa la nueva funcion authenticate redefinida
        user = authenticate(request=request, username=nomUsuario, password=pwdEnviada)
        logging.info('login: Se termina de autenticar el usuario')
        if user is not None:
            request.session['usuario'] = user.usr
            token = api.generar_token()
            logging.info('login: Se genera el token')
            user.token = token
            api.enviar_token(token, user.chat_id)
            logging.info('login: Se envia el token: ' + token )
            user.save()
            logging.info('login: Se guarda el token en el usuario')
            request.session['token'] = True
            # JBarradas(08-05-2020): Se pasa a página donde se ingresará el token
            return redirect("solicitar_token")
        else:
            logging.error('login: El usuario [ ' + nomUsuario + ' ] no existe')
            return render(request, 'login.html', {"user_form": user_form, "errores": "Usuario y contraseña inválidos."})
            
    elif request.method == "GET":
        return render(request, "login.html", {"user_form": user_form})


@decoradores.esperando_token
def solicitar_token(request):
    logging.info('solicitar_token: Se hace petición por el método: ' + request.method )
    token_form = tokenForm()
    usuario = None
    if request.method == "POST":
        request.session['token'] = False
        tokenUsuario = request.POST.get("token")
        try:  # JBarradas(22/05/2020): Se agrega por que manda error cuando el qry no hace match
            usuario = Usuario.objects.get(token=tokenUsuario)
        except:
            logging.error('solicitar_token: token no encontrado')
            return render(request, 'login.html', {"errores": "Token inválido.", "user_form": userForm()})
        if usuario is not None:
            usuario.token = '0'
            usuario.save()
            logging.info('solicitar_token: Se limpia el token al usuario: ' + usuario.usr)
            if usuario.usr == request.session.get("usuario"):
                request.session['logueado'] = True
                request.session.set_expiry(settings.EXPIRY_TIME)  # 5 horas
                return redirect("servidores")
        logging.error('solicitar_token: El token no es valido.')
        return render(request, 'login.html', {"errores": "Token inválido.", "user_form": userForm()})
        
    else:
        return render(request, "esperando_token.html", {"token_form": token_form})


@decoradores.esta_logueado
def servidores(request):
    # JABM (09-05-2020): Se agrega vista para página de servidores
    logging.info('servidores: Se intento una petición por el método: ' + request.method )
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        try:
            usuario = Usuario.objects.get(usr=nom_usuario)
            servidores = Servidor.objects.filter(estado=True,usr=usuario)
            contexto = {"usuario":usuario,"servidores":servidores}
            return render(request, "servidores.html",contexto)
        except:
            logging.error('servidores: Ocurrio un error al cargar datos. Usr: ' + nom_usuario)
            return render(request, "servidores.html",{"error": True})
        

def monitoreo(request,pk):
    logging.info('monitoreo: Se intento una petición por el método: ' + request.method )
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        try:
            usuario = Usuario.objects.get(usr=nom_usuario)
        except:
            logging.error('monitoreo: No se encontró el usuario: ' + nom_usuario)
            return render(request, "monitoreo.html",{'error': True})
        try:
            id_srv = pk
            servidor = Servidor.objects.get(estado=True,id=id_srv)
        except:
            logging.error('monitoreo: No se encontró el servidor: ' + id_srv)
            return render(request, "monitoreo.html",{'error': True})
        datos_servidor=api.solicitar_datos_srv(id_srv,servidor)
        return render(request, "monitoreo.html",{"usuario":usuario,"servidor":datos_servidor, "error": False})

def monitoreo_ajax(request,pk):
    logging.info('monitoreo_ajax: Se intento una petición por el método: ' + request.method )
    try:
        id_srv = pk
        servidor = Servidor.objects.get(estado=True,id=id_srv)
    except:
        logging.error('monitoreo: No se encontró el servidor: ' + id_srv)
        return render(request, "monitoreo.html",{'error': True})
    datos_servidor=api.solicitar_datos_srv(id_srv,servidor)
    return JsonResponse({ 
        'status': 200,
        'data': datos_servidor,
        'message': 'Ocurrió un error al procesar solicitud',
         })
    #datos_servidor=api.solicitar_datos_srv(id_srv,servidor)


# MML Se crea la funcion vista para el logout
@decoradores.esta_logueado
def logout(request):
    logging.info('logout: Se intento una petición por el método: ' + request.method )
    request.session.flush()
    return redirect("login")


###########################Vistas del administrador global #############################

def logoutAdmin(request):
    logging.info('logoutAdmin: Se intento una petición por el método: ' + request.method )
    do_logout(request) #MML se les tuvo que cambiar el nombre
    return HttpResponseRedirect('/accounts/login')


@axes_dispatch
@decoradores.no_esta_logueado
@decoradores.esta_logueado_global
def login_global(request):
    logging.info('login_global: Se intento una petición por el método: ' + request.method )
    admin_form = FormularioLogin
    if request.method == "POST":
        nomUsuario = request.POST.get("username")
        pwdEnviada = request.POST.get("password")
        user = authenticate(request=request, username=nomUsuario, password=pwdEnviada) # Aqui no usa nuestro backend si no el de django
        logging.info('login_global: Se termina de utilizar authenticate')
        if user is not None:
            try:
                token = api.generar_token()
                gtoken = Tglobal.objects.get(user=user.id)
                gtoken.token = token
                gtoken.save()
                logging.info('login_global: Se guarda token en base de datos.')
                request.session['global'] = True
                do_login(request,user) # MML requiere un request
                return redirect('global:index')
            except Exception as error:
                logging.error('login_global: ' + error.args[0])
                return render(request, 'global/login_global.html', {"form": admin_form, "errores": "Error al iniciar sesión"})
            
        else:
            logging.error('login_global: El usuario' + nomUsuario + 'no existente')
            return render(request, 'global/login_global.html', {"form": admin_form, "errores": "Usuario y contraseña inválidos."})
    elif request.method == "GET":
        return render(request, "global/login_global.html", {"form": admin_form})

@decoradores.esperando_token
def solicitar_token_global(request):
    logging.info('solicitar_token_global: Se intento una petición por el método: ' + request.method )
    token_form = tokenForm()
    usuario = None
    if request.method == "POST":
        tokenUsuario = request.POST.get("token")
        try:  # JBarradas(22/05/2020): Se agrega por que manda error cuando el qry no hace match
            usuario = Usuario.objects.get(token=tokenUsuario)
        except:
            logging.error('solicitar_token_global: No se localizó el token en la tabla usuarios: ' + tokenUsuario )
            return render(request, 'global/login_global.html', {"form": FormularioLogin, "errores": "Token inválido."})
        if usuario is not None:
            request.session['logueado'] = True
            request.session['usuario'] = usuario.usr
            request.session.set_expiry(settings.EXPIRY_TIME)  # 5 horas
            return redirect("servidores")
        else:
            return render(request, 'esperando_token.html', {"token_form": token_form, "errores": "Token inválido"})
    else:
        return render(request, "esperando_token.html", {"token_form": token_form})


class Inicio(TemplateView):
    template_name = 'global/index.html'


class ListarAdministrador(ListView):
    model = Usuario
    template_name = 'global/listar_admin.html'
    context_object_name = 'admins'
    queryset = Usuario.objects.all()


class ActualizarAdministrador(UpdateView):
    model = Usuario
    form_class = AdminForm
    template_name = 'global/crear_admin.html'
    success_url = reverse_lazy('global:listar_admin')


class CrearAdministrador(CreateView):
    model = Usuario
    form_class = AdminForm
    template_name = 'global/crear_admin.html'
    success_url = reverse_lazy('global:listar_admin')


class EliminarAdministrador(DeleteView):
    model = Usuario

    def post(self, request,pk, *args, **kwargs):
        object = Usuario.objects.get(usr = pk)
        object.delete()
        return redirect("global:listar_admin")


class CrearServer(CreateView):
    model = Servidor
    form_class = ServerForm
    template_name = 'global/crear_server.html'
    success_url = reverse_lazy('global:listar_server')


class ListarServidor(ListView): # MML esta incompleto
    model = Servidor
    template_name = 'global/listar_server.html'
    context_object_name = 'servers'
    queryset = Servidor.objects.all()


class ActualizarServidor(UpdateView):
    model = Servidor
    form_class = ServerForm
    template_name = 'global/server.html'
    success_url = reverse_lazy('global:listar_server')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servers'] = Servidor.objects.filter(estado=True)
        return context


class EliminarServidor(DeleteView):
    model = Servidor

    def post(self, request,pk, *args, **kwargs):
        object = Servidor.objects.get(id = pk)
        object.estado = False
        object.save() # MML solo el objeto tiene la propidad save() por lo tanto un filter no funciona
        return redirect('global:listar_server')