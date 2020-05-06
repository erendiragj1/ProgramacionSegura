from django.shortcuts import render, redirect
from .forms import *
import os
from .models import Usuario
import requests
import base64
import random
import string


# Create your views here.
def login(request):
    if request.method == "POST":
        user_form = userForm(request.POST)
        print(request.POST)
        print("loggin post")
        # if user_form.is_valid():
        print("Es valido")
        nomUsuario = request.POST.get("usr")
        print(nomUsuario)
        usuario = Usuario.objects.get(usr=nomUsuario)
        token = generar_token()
        usuario.token = token
        enviar_token(token, usuario.chat_id)
        usuario.save()
        return redirect("solicitar_token")
        # else:
        # print(user_form.errors)
    elif request.method == "GET":
        user_form = userForm()
        print(user_form)
        return render(request, "login.html", {"user_form": user_form})


def solicitar_token(request):
    if request.method == "POST":
        token_form = tokenForm(request.POST)
        print(request.POST)
        if token_form.is_valid():
            print("Si pudo !")
        else:
            print("No el pobre no pudo =(")
    else:
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
