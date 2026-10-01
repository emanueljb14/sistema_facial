from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def iniciar_sesion(request):
    """Maneja el inicio de sesión tradicional (Usuario y Contraseña)"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')


def cerrar_sesion(request):
    """Cierra la sesión actual y redirige al login"""
    logout(request)
    return redirect('usuarios:login')


@login_required(login_url='usuarios:login')
def lista_trabajadores(request):
    """Renderiza la lista de trabajadores/usuarios registrados"""
    return render(request, 'usuarios/lista.html')


def registro(request):
    """Renderiza y gestiona el registro de nuevos usuarios o trabajadores"""
    if request.method == 'POST':
        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('usuarios:lista_trabajadores')

    return render(request, 'usuarios/registro.html')


@login_required(login_url='usuarios:login')
def perfil(request):
    """Renderiza el perfil del usuario autenticado"""
    return render(request, 'usuarios/index.html')