from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .forms import *
from .models import Usuario
import requests
import random
import string
import datetime
from appWeb import decoradores
from django.http import HttpResponse
from axes.decorators import axes_dispatch


# Create your views here.

@axes_dispatch
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
            print("\t\ŧEl usuario existe y es: ", user)
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
    BOT_TOKEN = "1223842209:AAFeSFdD7as7v8ziRJwmKpH95W0rr48o81w"
    send_text = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=Markdown&text=%s' % (
        BOT_TOKEN, chatid, token)
    response = requests.get(send_text)


@decoradores.esta_logueado
def servidores(request):
    # JABM (09-05-2020): Se agrega vista para página de servidores
    print("servidores")
    if request.method == "GET":
        return render(request, "servidores.html")
