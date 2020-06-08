from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import cmac
import sys
import os
import base64


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


def generar_mac(llave, contenido_cifrado):
    # Función para generar mac
    cmac_cifrador = cmac.CMAC(algorithms.AES(llave), backend=default_backend())
    cmac_cifrador.update(contenido_cifrado)
    return cmac_cifrador.finalize()


pwd = sys.argv[1].encode('utf-8')  # Contraseña a cifrar
# Se guarda en una variable a la hora de cargar el servicio
llave_aes = os.urandom(32)
print("llave aes en binario",llave_aes)
llave_aes_b64 = base64.b64encode(llave_aes).decode('utf-8')
print("clave aes en base64",llave_aes_b64)
# Esta mac se agrega descifrada (no se cifra) al inicio de la contraseña cifrada
llave_mac = os.urandom(16)

print("\tSe cifrará la siguiente contraseña: \n", pwd)
pwd_cifrada = cifrar_mensaje(pwd, llave_aes, llave_mac)
print("\tSe cifro la contraseña:\n", pwd_cifrada)
# la mac se usa para revisar integridad
mac = generar_mac(llave_mac, pwd_cifrada)
print("\tSe saca la mac:\n", mac)
pwd_a_enviar = mac + pwd_cifrada
print("\tEsta es la contraseña a enviar:\n", pwd_a_enviar)
pwd_cifrada_b64 = base64.b64encode(pwd_cifrada).decode('utf-8')
print("\tContraseña en base 64\n", pwd_cifrada_b64)
mac_b64s = base64.b64encode(mac).decode('utf-8')
print("\tContraseña en mac b64\n", base64.b64encode(mac).decode('utf-8'))
print("\tTamaño de mac b64:\n", len(mac_b64s))
mac_pwd_b64 = mac_b64s + pwd_cifrada_b64
print("\tMac + Contraseña en base 64\n",mac_pwd_b64)

print("-.- -.- -.- Se descifra el mensjae en binario-.- -.- -.-")
pwd_sin_mac = pwd_a_enviar[16:]  # Se quita la mac a la pwd cifrada
pwd_descifrada = decifrar_mensaje(pwd_sin_mac, llave_aes, llave_mac)
print("\tMensaje descifrado: ", pwd_descifrada.decode('utf-8'))

print("-.- -.- -.- Se descifra el mensjae en base64 -.- -.- -.-")
pwd_sin_mac_b64 = mac_pwd_b64[24:] # 24 es la longuitud de la MAC en base64
print("contraseña como cadena")
print(pwd_sin_mac_b64)
pwd_sin_mac_b64_binario = base64.b64decode(pwd_sin_mac_b64.encode('utf-8'))
print("\tContraseña sin mac decode b64 en binario\n",pwd_sin_mac_b64_binario)
pwd_descifrada = decifrar_mensaje(pwd_sin_mac_b64_binario, llave_aes, llave_mac)
print("Contraseña decifrada binario",pwd_descifrada)
print("\tMensaje descifrado: ", pwd_descifrada.decode('utf-8'))
