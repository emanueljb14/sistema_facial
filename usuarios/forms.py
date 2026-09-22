
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Trabajador


class RegistroTrabajadorForm(forms.ModelForm):

    username = forms.CharField(
        label='Usuario',
        max_length=150
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )

    password_confirmacion = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Trabajador
        fields = [
            'dni',
            'nombres',
            'apellidos',
            'correo',
            'cargo',
            'area',
            'rol',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Este usuario ya existe.'
            )

        return username

    def clean_correo(self):
        correo = self.cleaned_data['correo']

        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError(
                'Este correo ya está registrado.'
            )

        return correo

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmacion = cleaned_data.get(
            'password_confirmacion'
        )

        if password and password_confirmacion:
            if password != password_confirmacion:
                raise forms.ValidationError(
                    'Las contraseñas no coinciden.'
                )

        return cleaned_data


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su usuario'
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su contraseña'
            }
        )
    )