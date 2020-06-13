import hashlib
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

class LoginBackend(BaseBackend):
    # MML se crea nuestro propio back-end de authenticacion, 
    # se redefinen los metodos predefinidos de Django
    def authenticate(self, request, username=None, password=None, **kwargs): # password anfsodbs
        print("Si entro al backend")
        # terminaSalt = 8  # MML Es la posicion donde termina el salt
        try:
            user = User.objects.get(username=username)
        except Exception:
            print("El usuario no existe")
            return None

        llave_aes_b64 = '+w4cEgqzBN1KVUlapQwL5KuHgc1gh8zVjBEQHP+y9fs='
        llave_aes = base64.b64decode(llave_aes_b64.encode('utf-8'))
        print(llave_aes)
        mac = 'utKTZxUrAkf7liJeEhC3pw=='
        llave_mac = base64.b64decode(mac.encode('utf-8'))
        pwdBD = user.password # pkbil 32fnb2i4bbs
        print(pwdBD)
        pwd_sin_mac_b64_binario = base64.b64decode(password.encode('utf-8'))
        print("\tContraseña sin mac decode b64 en binario\n", pwd_sin_mac_b64_binario)
        pwd_descifrada = decifrar_mensaje(pwd_sin_mac_b64_binario, llave_aes, llave_mac)
        print("binario pwd decifrada",pwd_descifrada)
        print("\tMensaje descifrado: ", pwd_descifrada.decode('utf-8'))

        pwd_valida = check_password(pwd_descifrada.decode('utf-8'), pwdBD)
        if pwd_valida:
            return user
        else:
            return None

        # hashBd = pwdBD[terminaSalt:]
        # saltBd = pwdBD[:terminaSalt]
        # md5 = hashlib.md5()
        # md5.update(password.encode("UTF-8") + saltBd.encode("UTF-8"))
        # hashObtenido = md5.hexdigest()
        # print(hashObtenido)
        # print(hashBd)
        # if hashObtenido == hashBd:
        #     return user
        # else:
        #     return None

    def get_user(self, user_id):
        try:
            return User.objects.get(usr=user_id)
        except User.DoesNotExist:
            return print("NADA")


def decifrar_mensaje(mensaje_cifrado, llave, vector):
    print("Aqui imprimimos todos los params",mensaje_cifrado,llave,vector)
    # Fuinción que regresa el mensaje descifrado
    aesCipher = Cipher(algorithms.AES(llave),
                       modes.CTR(vector),
                       backend=default_backend())
    decifrador = aesCipher.decryptor()
    mensaje_decifrado = decifrador.update(mensaje_cifrado)
    print("Funcion decifrando mensaje",mensaje_decifrado)
    mensaje_decifrado += decifrador.finalize()
    return mensaje_decifrado