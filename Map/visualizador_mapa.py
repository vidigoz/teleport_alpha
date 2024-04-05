import folium
import datetime,requests, geocoder
from teleport_app.models import TeleportDatabase
import json

def cargar_marcadores_desde_db():
    g = geocoder.ip('me')
    map_osm = folium.Map(location=[g.lat, g.lng], zoom_start=10)
    
    ref_fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print(ref_fecha)
    #objetos_db = TeleportDatabase.objects.filter(fecha_hora_cad__gt=ref_fecha)
    data = requests.get('http://localhost:8000/obtener_mensaje/')
    objetos_db = data.json()

    for datos in objetos_db['datos']:
        userid = datos['userid']
        usuario = datos['usuario']
        message = datos['message']
        latitude = datos['latitude'] 
        longitude = datos['longitude']    
        fechayhora = datos['fechayhora']
        fecha_hora_cad = datos['fecha_hora_cad']
        dbid = datos['id']
        enlace = 0
        hashtags = 0 

        # Crear el contador regresivo con JavaScript

        marker = folium.Marker(location=[float(latitude), float(longitude)]) 
        popup_html = f'''
        <div style="position: relative; display: inline-block; min-width: 125px ;padding: 5px; background-color: 
        rgba(255, 255, 255, 0.8); border: 2px solid black; border-radius: 
        5px; font-family: Arial; font-size: 12pt;">
        @<b>{usuario}:</b>\n
        {message}\n\n
        {enlace}\n\n
        {hashtags}\n\n
        <i>IDDB:{dbid}</i>
        </div>
        '''
        #<i>{contador_js}:</i>

        popup = folium.Popup(html=popup_html, max_width=250)
        # Asociar el popup al marcador
        marker.add_child(popup)

        # Añadir el marcador al mapa
        marker.add_to(map_osm)
        map_osm.save('teleport_app/templates/map/index.html')
    
    
#cargar_marcadores_desde_db()


    
   
