import hashlib
import secrets
import random
import string
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.contrib.auth.hashers import make_password, check_password
import logging
from django.conf import settings
import json
from os import environ
#PATH_LOG: Se define en el archivo de settings.py
logging.basicConfig(filename=settings.PATH_LOG, format='%(asctime)s %(message)s', level=logging.DEBUG)
# Excepciones


class ConeccionSrvMonitor(Exception):
    pass


def validar_password(pwd_enviada, pwd_bd):
    return check_password(pwd_enviada, pwd_bd)


def hashear_contrasena(password):
    return make_password(password)


def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def generar_token():
    tam_token = 12
    token = randomString(tam_token)
    return token

def limpiar_token(o_usuario):
    o_usuario.token=''
    o_usuario.save()
    return True


def limpiar_token_global(o_usuario):
    o_usuario.token=''
    o_usuario.save()
    return True


def enviar_token(token, chatid):
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


def regresar_token_solicitud(response):
    # Función que regresa el token dentro de la respuesta al autenticar con la appMonitor.
    # Response: Respuesta en string de la appMonitor.
    return response[1:-1].split(':')[1][1:-1]


def regresar_datos_srv(json_data):
    # Función que regresa la información del servidor, recibe el json resultante después de autenticar
    # con appMonitor
    data_full = json_data[1:-1].split(',')
    cpu = data_full[0].split(':')[1].strip('"')
    memoria = data_full[1].split(':')[1].strip('"')
    disco = data_full[2].split(':')[1].strip('"')
    return {"cpu": cpu, "disco": disco, "ram": memoria}


def solicitar_datos_srv(id_srv, servidor):
    # Función que solicita datos al servidor monitoreado
    # Regresa un diccionario para mostrar esa información.
    # Parámetros
    # servidor: Objeto del modulo servidor con datos como: ip, puerto...
    #
    url_srv = settings.PROTOCOLO_MONITOR+servidor.ip_srv+':'+str(servidor.puerto)
    logging.info('api.solicitar_datos_srv: url del servidor a monitorear: ' + url_srv)
    data = {'username': servidor.usr_srv,
            'password': servidor.llave+servidor.pwd_srv}
    logging.info('api.solicitar_datos_srv: Datos a consultar: ' + str(data))
    datos_servidor=datos_servidor={"status_code": 404}
    environ['REQUESTS_CA_BUNDLE']=settings.CERT_MONITOR #Se agrega el path del certificado para acreditar confianza al srv de monitoreo
    logging.info('monitoreo: Path cert: ' + str(settings.CERT_MONITOR) )
    try:
        solicitud = requests.post(url_srv+'/authenticacion/', data=data)
        logging.info('api.solicitar_datos_srv: Resultado de solicitud: ' + solicitud.text)
        if solicitud.status_code != 200:
            raise ConeccionSrvMonitor('Error al autenticar el servidor: ' + str(solicitud.status_code))
        srv_token = regresar_token_solicitud(solicitud.text)
        dir_headers = {'Authorization': 'Token ' + srv_token}
        solicitud = requests.get(url_srv+'/datos_monitor/', headers=dir_headers)
        logging.info('api.solicitar_datos_srv: Resultado de datos de monitor: ' + solicitud.text)
        if solicitud.status_code != 200:
            raise ConeccionSrvMonitor('Error al tomar información de el servidor: ' + str(solicitud.status_code))
        datos_servidor = regresar_datos_srv(json.loads(solicitud.text))
        datos_servidor.update(  {"srv_ip": servidor.ip_srv, "srv_puerto": servidor.puerto, "id_srv": id_srv, "status_code": 200})
        logging.info('api.solicitar_datos_srv: Datos del servidor: ' +  str(datos_servidor))
    except ConeccionSrvMonitor as error:
        logging.error('api.solicitar_datos_srv: Ocurrió un error al consultar datos al servidor: ' +  str(datos_servidor + 'el error es: ' + error))
        datos_servidor={"status_code": 401}#Se limpia en caso de que el error haya sido al actualizar diccionario
    finally:
        environ['REQUESTS_CA_BUNDLE']='' #Se regresa al valor de la variable original de entorno REQUESTS_CA_BUNDLE
    return datos_servidor #Si ocurrió un error este irá vacio.