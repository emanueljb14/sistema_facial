import re
import json
import base64
import io
import face_recognition

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from usuarios.models import Trabajador


# ==============================================================================
# CONFIGURACIÓN DE ESTRICTEZ / TOLERANCIA
# ==============================================================================
# Tolerancia predeterminada de face_recognition = 0.6
TOLERANCIA_RECONOCIMIENTO = 0.5


def calcular_porcentaje_similitud(distancia, tolerancia=TOLERANCIA_RECONOCIMIENTO):
    """
    Convierte la distancia euclidiana entre dos rostros en un porcentaje de similitud (0% a 100%).
    """
    if distancia > tolerancia:
        rango = 1.0 - tolerancia
        delta = distancia - tolerancia
        similitud = max(0.0, (1.0 - (delta / rango)) * 0.5)
    else:
        rango = tolerancia
        similitud = 1.0 - (distancia / (rango * 2))

    return round(similitud * 100, 2)


@login_required(login_url='usuarios:login')
def index(request):
    """Renderiza la pantalla del módulo de reconocimiento dentro del panel"""
    return render(request, 'reconocimiento/index.html')


@login_required(login_url='usuarios:login')
def dashboard(request):
    """Carga la plantilla del dashboard"""
    return render(request, 'dashboard/index.html')


def login_facial(request):
    """
    Renderiza la ventana pública de inicio de sesión facial.
    """
    return render(request, 'reconocimiento/login_facial.html')


def base64_to_cv2(base64_string):
    """Convierte Base64 en un objeto de imagen legible por face_recognition en memoria"""
    img_data = re.sub('^data:image/.+;base64,', '', base64_string)
    img_bytes = base64.b64decode(img_data)
    image_stream = io.BytesIO(img_bytes)
    return face_recognition.load_image_file(image_stream)


@csrf_exempt
def register_face(request):
    """Registra la foto biométrica guardándola directamente en PostgreSQL"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identifier = data.get('username')
            image_data = data.get('image')

            if not identifier or not image_data:
                return JsonResponse({'status': 'error', 'message': 'Faltan datos de registro.'}, status=400)

            trabajador = Trabajador.objects.filter(dni=identifier).first()
            if not trabajador:
                trabajador = Trabajador.objects.filter(usuario__username=identifier).first()

            if not trabajador:
                return JsonResponse({'status': 'error', 'message': 'El DNI o usuario no está registrado en el sistema.'}, status=404)

            # Validar si se detecta rostro
            face_img = base64_to_cv2(image_data)
            encodings = face_recognition.face_encodings(face_img)

            if len(encodings) == 0:
                return JsonResponse({'status': 'error', 'message': 'No se detectaron coordenadas faciales. Enfoca mejor tu rostro.'}, status=400)

            # Guardar cadena Base64 en la base de datos
            trabajador.foto = image_data
            trabajador.save()

            return JsonResponse({'status': 'success', 'message': f'Rostro guardado correctamente para {trabajador.nombres}.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error en el registro: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


@csrf_exempt
def login_face(request):
    """
    Autentica a un trabajador verificando que el rostro capturado coincida 
    únicamente con el DNI ingresado (Validación 1 a 1).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dni_ingresado = data.get('dni', '').strip()
            image_data = data.get('image')

            if not dni_ingresado or not image_data:
                return JsonResponse({'status': 'error', 'message': 'Ingrese su DNI y capture su rostro.'}, status=400)

            # 1. BUSCAR TRABAJADOR POR DNI O USERNAME
            trabajador = Trabajador.objects.filter(dni=dni_ingresado, activo=True).first()
            if not trabajador:
                trabajador = Trabajador.objects.filter(usuario__username=dni_ingresado, activo=True).first()

            if not trabajador:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'El DNI o usuario "{dni_ingresado}" no existe o está inactivo.'
                }, status=404)

            # 2. VERIFICAR QUE EL TRABAJADOR TENGA REGISTRO FACIAL
            if not trabajador.foto:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'El usuario {trabajador.nombres} no tiene un registro facial guardado.'
                }, status=400)

            # 3. VERIFICAR QUE TENGA UN USUARIO ASOCIADO PARA INICIAR SESIÓN
            if not trabajador.usuario:
                return JsonResponse({
                    'status': 'error',
                    'message': f'El trabajador ({trabajador.nombres}) no tiene un usuario asignado en el sistema.'
                }, status=400)

            # 4. DECODIFICAR Y PROCESAR LA IMAGEN DE LA CÁMARA
            login_img = base64_to_cv2(image_data)
            login_encodings = face_recognition.face_encodings(login_img)

            if len(login_encodings) == 0:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'No se detectó un rostro válido frente a la cámara.',
                    'similitud': 0.0
                }, status=400)

            login_encoding = login_encodings[0]

            # 5. DECODIFICAR Y PROCESAR LA IMAGEN REGISTRADA DEL TRABAJADOR
            registered_img = base64_to_cv2(trabajador.foto)
            registered_encodings = face_recognition.face_encodings(registered_img)

            if len(registered_encodings) == 0:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'No se pudo leer la foto registrada de este usuario en la base de datos.',
                    'similitud': 0.0
                }, status=400)

            registered_encoding = registered_encodings[0]

            # 6. CALCULAR DISTANCIA FACIAL Y PORCENTAJE DE SIMILITUD
            distancia = face_recognition.face_distance([registered_encoding], login_encoding)[0]
            porcentaje_similitud = calcular_porcentaje_similitud(distancia, tolerancia=TOLERANCIA_RECONOCIMIENTO)

            # 7. COMPARAR SEGÚN LA TOLERANCIA ESTABLECIDA
            match = distancia <= TOLERANCIA_RECONOCIMIENTO

            if match:
                login(request, trabajador.usuario)
                return JsonResponse({
                    'status': 'success', 
                    'message': f'¡Bienvenido {trabajador.nombres}!',
                    'similitud': porcentaje_similitud,
                    'distancia': round(float(distancia), 4),
                    'tolerancia': TOLERANCIA_RECONOCIMIENTO,
                    'foto_registrada': trabajador.foto,  # <--- INCLUYE LA FOTO REGISTRADA
                    'redirect_url': '/dashboard/'
                })
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Verificación fallida: El rostro no corresponde al DNI/Usuario {dni_ingresado}.',
                    'similitud': porcentaje_similitud,
                    'distancia': round(float(distancia), 4),
                    'tolerancia': TOLERANCIA_RECONOCIMIENTO,
                    'foto_registrada': trabajador.foto  # <--- INCLUYE LA FOTO PARA MOSTRARLA
                }, status=401)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error en el servidor: {str(e)}'}, status=500)

    return render(request, 'reconocimiento/login_facial.html')