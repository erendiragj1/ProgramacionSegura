import hashlib
import sys
import secrets

salt = secrets.token_hex(4).encode("utf-8")
password = sys.argv[1]

m = hashlib.md5()
m.update(password.encode('utf-8')+salt)
miHash = m.hexdigest()
contrasena = salt.decode("utf-8") + miHash
print(len(contrasena))
print(contrasena)
# usr = miguel, pwd = miguelPS_2020, nombres = miguel, apellidos = Monroy Lara, correo = miguel@proySegura.com, numero = 2282687760, chatid = 494665300
