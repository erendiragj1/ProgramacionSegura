import hashlib
from .models import Usuario
from django.contrib.auth.backends import BaseBackend


class LoginBackend(BaseBackend):
    # MML se crea nuestro propio back-end de authenticacion, se redefinen los metodos predefinidos de Django
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Si entro")
        terminaSalt = 8  # Es la posicion donde termina el salt
        try:
            user = Usuario.objects.get(usr=username)
        except Exception:
            print("El usuario no existe")
            return None

        pwdBD = user.pwd
        hashBd = pwdBD[terminaSalt:]
        saltBd = pwdBD[:terminaSalt]
        md5 = hashlib.md5()
        md5.update(password.encode("UTF-8") + saltBd.encode("UTF-8"))
        hashObtenido = md5.hexdigest()
        print(hashObtenido)
        print(hashBd)
        if hashObtenido == hashBd:
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(usr=user_id)
        except Usuario.DoesNotExist:
            return print("NADA")
