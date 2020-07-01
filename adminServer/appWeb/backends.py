import hashlib
from .models import Usuario
from django.contrib.auth.backends import BaseBackend
from .api import validar_password

class LoginBackend(BaseBackend):
    # MML se crea nuestro propio back-end de authenticacion, se redefinen los metodos predefinidos de Django
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(usr=username)
        except Exception:
            return None

        pwdBD = user.pwd
        if validar_password(password,pwdBD):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(usr=user_id)
        except Usuario.DoesNotExist:
            return print("NADA")
