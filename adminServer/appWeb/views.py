from django.shortcuts import render, redirect
from .forms import *
import os
from .models import Usuario
import requests
import random
import string
import hashlib
from appWeb import decoradores
# Create your views here.


def login(request):
    if request.method == "POST":
        user_form = userForm(request.POST)
        print(request.POST)
        nomUsuario = request.POST.get("usr")
        pwdEnviada = request.POST.get("pwd")
        print(nomUsuario)
        usuario = Usuario.objects.get(usr=nomUsuario)
        if usuario is not None:
            password_usuario = usuario.pwd
            print(password_usuario)
            if validar_contrasena(pwdEnviada, password_usuario):
                token = generar_token()
                usuario.token = token
                print('\t\t Su token')
                print(token)
                print('\t\t * * * * *')
                enviar_token(token, usuario.chat_id)
                usuario.save()
                request.session['token'] = True #JBarradas(08-05-2020): Se pasa a página de token
            else:
                return redirect("login")
        return redirect("solicitar_token")
        # else:
        # print(user_form.errors)
    elif request.method == "GET":
        user_form = userForm()
        print(user_form)
        return render(request, "login.html", {"user_form": user_form})

@decoradores.esperando_token
def solicitar_token(request):
    if request.method == "POST":
        print('\t\tEntro a solicitar_token por POST')
        token_form = tokenForm(request.POST)
        print(request.POST)
        if token_form.is_valid():
            print("Si pudo !")
        else:
            print("No el pobre no pudo =(")
    else:
        print('\t\tEntro a solicitar_token por OTRO')
        token_form = tokenForm()
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


def validar_contrasena(pwdEnviada, pwdBD):
    print("Si entro")
    terminaSalt = 8  # Es la posicion donde termina el salt
    hashBd = pwdBD[terminaSalt:]
    saltBd = pwdBD[:terminaSalt]
    md5 = hashlib.md5()
    md5.update(pwdEnviada.encode("UTF-8")+saltBd.encode("UTF-8"))
    hashObtenido = md5.hexdigest()
    print(hashObtenido)
    print(hashBd)
    if hashObtenido == hashBd:
        return True
    else:
        return False

@decoradores.esta_logueado
def servidores(request):
    #JABM (09-05-2020): Se agrega vista para página de 
    #servidores...
    pass