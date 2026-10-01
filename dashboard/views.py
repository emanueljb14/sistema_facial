from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='usuarios:login')
def dashboard_index(request):
    return render(request, 'dashboard/index.html')


@login_required(login_url='usuarios:login')
def usuarios_index(request):
    return render(request, 'usuarios/index.html')


@login_required(login_url='usuarios:login')
def reconocimiento_index(request):
    return render(request, 'reconocimiento/index.html')


@login_required(login_url='usuarios:login')
def asistencias_index(request):
    return render(request, 'asistencias/index.html')


@login_required(login_url='usuarios:login')
def reportes_index(request):
    return render(request, 'reportes/index.html')