from django import forms
from .models import Usuario


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
