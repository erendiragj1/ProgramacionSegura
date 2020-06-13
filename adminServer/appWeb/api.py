import hashlib
import secrets
import random
import string
import requests

def hashear_contrasena(password):
    salt = secrets.token_hex(4).encode("utf-8")
    m = hashlib.md5()
    m.update(password.encode('utf-8') + salt)
    miHash = m.hexdigest()
    contrasena = salt.decode("utf-8") + miHash
    print(len(contrasena))
    print(contrasena)
    return contrasena


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