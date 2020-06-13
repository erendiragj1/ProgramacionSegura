from django import forms
from . import api
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
    # MML verificacion de Contraseña
    pwd2 = forms.CharField(label= 'Contraseña de confirmación', widget= forms.PasswordInput(
        attrs= {
            'class':'form-control',
            'placeholder':'Ingrese de nuevo la contraseña',
            'id':'pwd2',
            'required':'required',
        }
    ))
    class Meta:
        model = Usuario
        fields = ['usr', 'pwd', 'nombres', 'apellidos', 'correo', 'numero','chat_id']
        labels = {
            'usr': 'Nombre de usuario',
            'pwd': 'Contraseña del administrador',
            'nombres': 'Nombre real del administrador',
            'apellidos': 'Apellidos del administrador',
            'correo': 'Correo del administrador',
            'numero': 'Numero del administrador',
            'chat_id': 'Chat id de Telegram'
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
            'chat_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el id del chat del administrador',
                    'id': 'chat_id'  # probablemente el id se deba cambiar al que tienen las plantillas
                }
            ),
        }
    def clean_pwd2(self): # MML Hacemos la verificacion de si la contraeña coincide
        pwd1 = self.cleaned_data['pwd']
        pwd2 = self.cleaned_data['pwd2']
        if pwd1 != pwd2:
            raise forms.ValidationError('Las contraseñas no coinciden') # Este es el error que esta en forms.error
        return pwd2

    def save(self, commit=True):
        user = super().save(commit=False) # MML se redefine la forma en que se guarda la contraseña
        pwd_hash = api.hashear_contrasena(self.cleaned_data['pwd'])
        user.pwd = pwd_hash
        if commit:
            user.save()
        return user


class ServerForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ('desc_srv', 'ip_srv', 'puerto', 'pwd_srv', 'usr', 'estado')
        label = {
            'desc_srv': 'Descrićión del servidor',
            'ip_srv': 'IP del servidor',
            'puerto': 'Puerto del servidor',
            'pwd_srv': 'Contraseña del servidor',
            'usr': 'Administrador del servidor',
            'estado': 'Estado del servidor'
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
            'estado': forms.CheckboxInput(),
        }

