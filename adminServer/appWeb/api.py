import hashlib
import secrets
import random
import string
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import cmac


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

def cifrar_mensaje(mensaje, llave, vector):
    # Función que regresa mensaje cifrado
    # Parametros:
    # mensaje -> En binario
    # llave -> En binario
    # vector -> En binario
    aesCipher = Cipher(algorithms.AES(llave),
                       modes.CTR(vector),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    mensaje_cifrado = cifrador.update(mensaje)
    cifrador.finalize()
    return mensaje_cifrado

def decifrar_mensaje(mensaje_cifrado, llave, vector):
    # Fuinción que regresa el mensaje descifrado
    aesCipher = Cipher(algorithms.AES(llave),
                       modes.CTR(vector),
                       backend=default_backend())
    decifrador = aesCipher.decryptor()
    mensaje_decifrado = decifrador.update(mensaje_cifrado)
    mensaje_decifrado += decifrador.finalize()
    return mensaje_decifrado