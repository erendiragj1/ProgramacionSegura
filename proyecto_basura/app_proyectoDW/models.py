from django.db import models

# Create your models here.

class Usuarios(models.Model):
    usr = models.CharField(max_length=12, primary_key=True )
    pwd = models.CharField(max_length=12, null=False)
    nombre = models.CharField(max_length=32, null=False)
    correo = models.CharField(max_length=32, null=True)

class Servidores(models.Model):
    id = models.AutoField(primary_key=True)
    desc_srv = models.CharField(max_length=32, null=False)
    ip_srv = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, null=False)
    status = models.CharField(max_length=1, null=False)
    fh_srv = models.DateTimeField(auto_now=False)