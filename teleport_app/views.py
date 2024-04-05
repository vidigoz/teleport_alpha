from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TeleportDatabase
import json, requests, geocoder
import datetime
from Map.visualizador_mapa import cargar_marcadores_desde_db

# Create your views here.

@csrf_exempt
def guardar_mensaje(request):
    if request.method == 'POST':
# Obtener datos del cuerpo de la solicitud
        data = json.loads(request.body)
# Agregar la fecha y hora actual
        fechayhora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['fechayhora'] = fechayhora
        fecha_hora_cad = datetime.datetime.now() + datetime.timedelta(hours=1)
        data['fecha_hora_cad'] = fecha_hora_cad.strftime("%Y-%m-%d %H:%M:%S")
        print(fechayhora)
        print(fecha_hora_cad)
        # Crear una instancia del modelo y guardarla en la base de datos
        TeleportDatabase.objects.create(
            userid=data.get('userid'),
            usuario=data.get('usuario'),
            message=data.get('message'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            fechayhora = data.get('fechayhora'),
            fecha_hora_cad = data.get('fecha_hora_cad'),   
        )
        # Devolver una respuesta JSON
        return JsonResponse({'status': 'Mensaje guardado correctamente.'})
    else:
        # Devolver un error si la solicitud no es POST
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
#------------------------------------------------------------
    
def obtener_mensaje(request):
    if request.method == 'GET':
        # Obtener todos los mensajes de la base de datos con filtro de fecha
        ref_fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(ref_fecha)
        mensajes = TeleportDatabase.objects.filter(fecha_hora_cad__gt=ref_fecha)
        if mensajes.exists():
            mensajes_data = []
            # Iterar sobre los mensajes y obtener los datos necesarios
            for mensaje in mensajes:
                mensaje_data = {
                    'id': mensaje.id,
                    'userid': mensaje.userid,
                    'usuario': mensaje.usuario,
                    'message': mensaje.message,
                    'latitude': mensaje.latitude,
                    'longitude': mensaje.longitude,
                    'fechayhora': mensaje.fechayhora,
                    'fecha_hora_cad': mensaje.fecha_hora_cad,
                    'show': mensaje.show,
                }
                print(mensaje.fechayhora)
                mensajes_data.append(mensaje_data)
            return JsonResponse({'datos': mensajes_data})
        else:
            return JsonResponse({'error': 'No hay mensajes disponibles.'}, status=404)
    else:
        # Devolver un error si la solicitud no es GET
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
#------------------------------------------------------------
def home(request):
   cargar_marcadores_desde_db()
   return render(request, 'map/index.html')

#------------------------------------------------------------

def home2(request):
    data = requests.get('http://localhost:8000/obtener_mensaje/')
    try:
            data.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return render(request, 'map_openStreetMap/error.html', {'error_message': 'No hay mensajes disponibles.'})
    g = geocoder.ip('me')
    user_location = [g.lat, g.lng]
    objetos_db = data.json()
    return render(request, 'map_openStreetMap/map.html', {'datos': objetos_db['datos'], 'user_location': user_location})

    
