from django import forms
from .models import *


class userForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['usr', 'pwd']
        labels = {
            'usr': 'Nombre de usuario',
            'pwd': 'Contraseña',
        }
        widgets = {
            'usr': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su usuario',
                    'name': 'usr',
                    'id': 'usr',
                }
            ),
            'pwd': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su contraseña',
                    'name': 'pwd',
                    'id': 'pwd',
                }
            )
        }


class tokenForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['token']
        labels = {
            'token': 'Ingresar Token: ',
        }
        widgets = {
            'token': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su token',
                    'name': 'token',
                    'id': 'token',
                }
            ),
        }


################# MML Forms del Admin global ########################

class AdminForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['usr', 'pwd', 'nombres', 'apellidos', 'correo', 'numero']
        labels = {
            'usr': 'Nombre de usuario',
            'pwd': 'Contraseña del administrador',
            'nombres': 'Nombre real del administrador',
            'apellidos': 'Apellidos del administrador',
            'correo': 'Correo del administrador',
            'numero': 'Numero del administrador',
        }

        widgets = {
            'usr': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el usario del administrador',
                    'id': 'usr'  # probablemente el id se deba cambiar al que tienen las plantillas
                }
            ),
            'pwd': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la contraseña del administrador',
                    'id': 'pwd'
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del administrador',
                    'id': 'nombres'  # probablemente el id se deba cambiar al que tienen las plantillas
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los apellidos del administrador',
                    'id': 'apellidos'  # probablemente el id se deba cambiar al que tienen las plantillas
                }
            ),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el correo del administrador',
                    'id': 'correo'  # probablemente el id se deba cambiar al que tienen las plantillas
                }
            ),
            'numero': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del administrador',
                    'id': 'numero'  # probablemente el id se deba cambiar al que tienen las plantillas
                }
            ),
        }


class ServerForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ('desc_srv', 'ip_srv', 'puerto', 'pwd_srv', 'usr')
        label = {
            'desc_srv': 'Descrićión del servidor',
            'ip_srv': 'IP del servidor',
            'puerto': 'Puerto del servidor',
            'pwd_srv': 'Contraseña del servidor',
            'usr': 'Administrador del servidor',
        }
        widgets = {
            'desc_srv': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pequeña descripcion',
                }
            ),
            'ip_srv': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'IP del nuevo servidor',
                }
            ),
            'puerto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'IP del nuevo servidor',
                }
            ),
            'pwd_srv': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'IP del nuevo servidor',
                }
            ),
            'usr': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
