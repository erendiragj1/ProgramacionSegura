from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *
from .models import Usuario,Servidor
import requests
import random
import string
from appWeb import decoradores
from axes.decorators import axes_dispatch
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
import json
# Create your views here.

@axes_dispatch
@decoradores.no_esta_logueado
def login(request):
    user_form = userForm()
    if request.method == "POST":
        # user_form = userForm(request.POST)
        nomUsuario = request.POST.get("usr")
        pwdEnviada = request.POST.get("pwd")
        # MML se usa la nueva funcion authenticate redefinida
        user = authenticate(
            request=request, username=nomUsuario, password=pwdEnviada)
        if user is not None:
            print("\t El usuario existe y es: ", user)
            token = generar_token()
            user.token = token
            enviar_token(token, user.chat_id)
            user.save()
            print(user.token)
            # JBarradas(08-05-2020): Se pasa a página de token
            request.session['token'] = True
            return redirect("solicitar_token")
        else:
            print('\t\ŧEl usuario no existe')
            return render(request, 'login.html', {"user_form": user_form, "errores": "Usuario y contraseña inválidos."})
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
        except:
            pass
        if usuario is not None:
            print(usuario.token)
            request.session['logueado'] = True
            request.session['usuario'] = usuario.usr
            request.session.set_expiry(18000)  # 5 horas
            return redirect("servidores")
        else:
            return render(request, 'esperando_token.html', {"token_form": token_form, "errores": "Token inválido"})
    else:
        print('\t\tEntro a solicitar_token por OTRO')

        return render(request, "esperando_token.html", {"token_form": token_form})


def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def generar_token():
    tam_token = 12
    token = randomString(tam_token)
    print(token)
    return token


def enviar_token(token, chatid):
    print("se empieza a enviar token")
    BOT_TOKEN = "1223842209:AAFeSFdD7as7v8ziRJwmKpH95W0rr48o81w"
    send_text = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=Markdown&text=%s' % (
        BOT_TOKEN, chatid, token)
    response = requests.get(send_text)


@decoradores.esta_logueado
def servidores(request):
    # JABM (09-05-2020): Se agrega vista para página de servidores
    print("servidores")
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        usuario = Usuario.objects.get(usr=nom_usuario)
        servidores = Servidor.objects.filter(estado=True,usr=usuario)
        contexto = {"usuario":usuario,"servidores":servidores}
        return render(request, "servidores.html",contexto)

def monitoreo(request,pk):
    if request.method == "GET":
        nom_usuario = request.session.get("usuario")
        usuario = Usuario.objects.get(usr=nom_usuario)
        id_srv = pk
        print("\t\t*-*-*Imprimiendo pk")
        print(id_srv)
        servidor = Servidor.objects.get(estado=True,id=id_srv)
        srv_llave_aes=servidor.llave
        srv_usr=servidor.usr.usr
        srv_pwd=servidor.pwd_srv
        srv_ip=servidor.ip_srv
        srv_puerto=servidor.puerto
        data = {'username': srv_usr, 'password': srv_pwd}
        print('http://'+srv_ip+':'+str(srv_puerto)+'/authenticacion/')
        solicitud = requests.post('http://'+srv_ip+':'+str(srv_puerto)+'/authenticacion/', data=data) 
        print("\t\ŧ*-*-*Imprimiendo status")
        print(solicitud.text)
        srv_token=solicitud.text[1:-1].split(':')[1][1:-1]
        dir_headers={'Authorization':'Token '+ srv_token}
        solicitud = requests.get('http://'+srv_ip+':'+str(srv_puerto)+'/datos_monitor/', headers=dir_headers)
        print(solicitud.text)
        #srv_datos_monitor=solicitud.text.strip()[1:-1].strip(' ').split(',')[2].split(':')
        print('\t\t\tDATOS MONITOR UwU')
        print(solicitud.text)
        print(solicitud.text.strip('\\'))
        json_data=json.loads(solicitud.text)
        print(json_data)
        data_full=json_data[1:-1].split(',')
        print(data_full)
        cpu=data_full[0].split(':')[1]
        memoria=data_full[1].split(':')[1]
        disco=data_full[2].split(':')[1]
        print(cpu)        
        print(memoria)
        print(disco)
        #Delete this 
        contexto = {"usuario":usuario,"servidores":servidores}
        return render(request, "servidores.html",contexto)
# MML Se crea la funcion vista para el logout
@decoradores.esta_logueado
def logout(request):
    request.session.flush()
    return redirect("login")


###########################Vistas del administrador global #############################


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
    queryset = Servidor.objects.filter(estado=True)


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