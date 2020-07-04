import hashlib
import sys
import secrets

salt = secrets.token_hex(4).encode("utf-8")
password = sys.argv[1]

m = hashlib.md5()
m.update(password.encode('utf-8')+salt)
miHash = m.hexdigest()
contrasena = salt.decode("utf-8") + miHash
# usr = miguel, pwd = miguelPS_2020, nombres = miguel, apellidos = Monroy Lara, correo = miguel@proySegura.com, numero = 2282687760, chat_id = 494665300
# usr = tony, pwd = tonyPS_2020, nombres = antonio, apellidos = Barradas Maldonado, correo = tony@proySegura.com, numero = 2285910491, chat:id = 494665300
