from django.contrib.auth import authenticate,login as do_login,logout as do_logout
from django.http import HttpResponseRedirect
from django.contrib.auth import signals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import *
from .models import Usuario,Servidor
import requests
from . import api
from appWeb import decoradores
from axes.decorators import axes_dispatch
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView
import json
import logging
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
# Create your views here.
from django.conf import settings

logging.basicConfig(filename='login.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

@axes_dispatch
@decoradores.no_esta_logueado
def login(request):
    user_form = userForm()
    if request.method == "POST":
        # user_form = userForm(request.POST)
        nomUsuario = request.POST.get("usr")
        pwdEnviada = request.POST.get("pwd")
        # MML se usa la nueva funcion authenticate redefinida
        user = authenticate(request=request, username=nomUsuario, password=pwdEnviada)
        if user is not None:
            print("\t El usuario existe y es: ", user)
            token = api.generar_token()
            user.token = token
            api.enviar_token(token, user.chat_id)
            user.save()
            print(user.token)
            # JBarradas(08-05-2020): Se pasa a página de token
            request.session['token'] = True
            return redirect("solicitar_token")
            logging.info('usuario valido')
        else:
            print('\t\ŧEl usuario no existe')
            return render(request, 'login.html', {"user_form": user_form, "errores": "Usuario y contraseña inválidos."})
            logging.info('error, el usuario no existente')
    elif request.method == "GET":
        return render(request, "login.html", {"user_form": user_form})


@decoradores.esperando_token
def solicitar_token(request):
    token_form = tokenForm()
    usuario = None
    if request.method == "POST":
        print('\t\tEntro a solicitar_token por POST')
        tokenUsuario = request.POST.get("token")
        try:  # JBarradas(22/05/2020): Se agrega por que manda error cuando el qry no hace match
            usuario = Usuario.objects.get(token=tokenUsuario)
            logging.info('usuario error')
        except:
            pass
        if usuario is not None:
            print(usuario.token)
            request.session['logueado'] = True
            request.session['usuario'] = usuario.usr
            request.session.set_expiry(settings.EXPIRY_TIME)  # 5 horas
            return redirect("servidores")
        else:
            return render(request, 'esperando_token.html', {"token_form": token_form, "errores": "Token inválido"})
            logging.info('error token')
    else:
        print('\t\tEntro a solicitar_token por OTRO')
        logging.info('token entro')
        return render(request, "esperando_token.html", {"token_form": token_form})


@decoradores.esta_logueado
def servidores(request):
    # JABM (09-05-2020): Se agrega vista para página de servidores
    print("servidores")
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        logging.info('usuario loguedo')
        usuario = Usuario.objects.get(usr=nom_usuario)
        servidores = Servidor.objects.filter(estado=True,usr=usuario)
        contexto = {"usuario":usuario,"servidores":servidores}
        return render(request, "servidores.html",contexto)

def monitoreo(request,pk):
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        usuario = Usuario.objects.get(usr=nom_usuario)
        id_srv = pk
        servidor = Servidor.objects.get(estado=True,id=id_srv)
        srv_llave_aes=servidor.llave
        srv_usr=servidor.usr.usr
        srv_pwd=servidor.pwd_srv
        srv_ip=servidor.ip_srv
        srv_puerto=servidor.puerto
        data = {'username': srv_usr, 'password': srv_llave_aes+srv_pwd, 
            'llave_aes_b64': srv_llave_aes}
        solicitud = requests.post('http://'+srv_ip+':'+str(srv_puerto)+'/authenticacion/', data=data) 
        srv_token=solicitud.text[1:-1].split(':')[1][1:-1]
        dir_headers={'Authorization':'Token '+ srv_token}
        solicitud = requests.get('http://'+srv_ip+':'+str(srv_puerto)+'/datos_monitor/', 
            headers=dir_headers)
        json_data=json.loads(solicitud.text)
        print("json_data")
        print(json_data)
        data_full=json_data[1:-1].split(',')
        cpu=data_full[0].split(':')[1].strip('"')
        memoria=data_full[1].split(':')[1].strip('"')
        disco=data_full[2].split(':')[1].strip('"')

        datos_servidor={"cpu": cpu, "disco": disco, "ram": memoria, 
            "srv_ip":srv_ip, "srv_puerto":srv_puerto, "id_srv": id_srv}

        contexto = {"usuario":usuario,"servidor":datos_servidor}
        return render(request, "monitoreo.html",contexto)


# MML Se crea la funcion vista para el logout
@decoradores.esta_logueado
def logout(request):
    request.session.flush()
    return redirect("login")


###########################Vistas del administrador global #############################
# #@method_decorator(never_cache)
# #@method_decorator(axes_dispatch)
# class LoginGlobal(FormView): #vista basada en clase
#     template_name = 'global/login_global.html'
#     form_class = FormularioLogin
#     success_url = reverse_lazy('global:index')
#
#
#     def dispatch(self, request, *args, **kwargs): # MML preguntamos al principio si el usuario esta authenticado por que dispatch es lo primero que se ejecuta
#         usr = request.POST.get("username")
#         pwd = request.POST.get("password")
#         print("Usuario y contraseña enviados", usr, pwd)
#         authenticate(request=request, username=usr, password=pwd)
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url()) # MML si lo esta lo llevamos a nuestra url de inicio, CON ESTO YA NO PUEDE REGRESAR A LA PAGINA DE LOGIN AUNQUE PONGA EN LA URL accounts/login
#         else:
#             signals.user_login_failed.send(sender=usr,request=request,credentials ={'username': usr,})
#             return super(LoginGlobal,self).dispatch(request,*args,**kwargs)
#
#     def form_valid(self, form):
#         do_login(self.request,form.get_user())
#         return super(LoginGlobal,self).form_valid(form)

def logoutAdmin(request):
    do_logout(request) #MML se les tuvo que cambiar el nombre
    return HttpResponseRedirect('/accounts/login')


@axes_dispatch
def login_global(request):
    admin_form = FormularioLogin
    if request.method == "POST":
        nomUsuario = request.POST.get("username")
        pwdEnviada = request.POST.get("password")
        user = authenticate(request=request, username=nomUsuario, password=pwdEnviada) # Aqui no usa nuestro backend si no el de django
        if user is not None:
            print(user)
            do_login(request,user) # MML requiere un request
            return redirect('global:index')
        else:
            print('\t\ŧEl usuario no existe')
            logging.info('error, el usuario no existente')
            return render(request, 'global/login_global.html', {"form": admin_form, "errores": "Usuario y contraseña inválidos."})
    elif request.method == "GET":
        return render(request, "global/login_global.html", {"form": admin_form})


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