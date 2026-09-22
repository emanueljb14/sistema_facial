
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistroTrabajadorForm
from .models import Trabajador


def lista_trabajadores(request):
    trabajadores = Trabajador.objects.all()

    return render(
        request,
        'usuarios/lista.html',
        {
            'trabajadores': trabajadores
        }
    )


def registro(request):

    if request.user.is_authenticated:
        return redirect('lista_trabajadores')

    if request.method == 'POST':
        form = RegistroTrabajadorForm(request.POST)

        if form.is_valid():

            trabajador = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            correo = form.cleaned_data['correo']

            usuario = User.objects.create_user(
                username=username,
                email=correo,
                password=password,
                first_name=trabajador.nombres,
                last_name=trabajador.apellidos
            )

            trabajador.usuario = usuario
            trabajador.save()

            messages.success(
                request,
                'Trabajador registrado correctamente.'
            )

            return redirect('login')

    else:
        form = RegistroTrabajadorForm()

    return render(
        request,
        'usuarios/registro.html',
        {
            'form': form
        }
    )


def iniciar_sesion(request):

    if request.user.is_authenticated:
        return redirect('lista_trabajadores')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            usuario = authenticate(
                request,
                username=username,
                password=password
            )

            if usuario is not None:

                try:
                    trabajador = usuario.trabajador

                    if not trabajador.activo:
                        messages.error(
                            request,
                            'Este usuario se encuentra inactivo.'
                        )

                        return redirect('login')

                except Trabajador.DoesNotExist:
                    pass

                login(request, usuario)

                messages.success(
                    request,
                    'Inicio de sesión correcto.'
                )

                return redirect('lista_trabajadores')

    else:
        form = LoginForm()

    return render(
        request,
        'usuarios/login.html',
        {
            'form': form
        }
    )


@login_required
def cerrar_sesion(request):

    logout(request)

    messages.success(
        request,
        'Sesión cerrada correctamente.'
    )

    return redirect('login')


@login_required
def perfil(request):

    trabajador = None

    try:
        trabajador = request.user.trabajador
    except Trabajador.DoesNotExist:
        pass

    return render(
        request,
        'usuarios/perfil.html',
        {
            'trabajador': trabajador
        }
    )