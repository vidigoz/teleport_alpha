import folium
import datetime
from teleport_app.models import TeleportDatabase

import json

def cargar_marcadores_desde_db():

    map_osm = folium.Map(location=[32.663334, -115.467781], zoom_start=3)
    # Conecta a la base de datos
    #response = requests.get('http://localhost:8000/obtener_mensaje/')
    ref_fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(ref_fecha)
 
    objetos_db = TeleportDatabase.objects.filter(fecha_hora_cad__gt=ref_fecha)
    for datos in objetos_db:

        userid = datos.userid
        usuario = datos.usuario
        message = datos.message
        latitude = str(datos.latitude)
        longitude = str(datos.longitude)
        fechayhora = datos.fechayhora
        dbid = datos.id

        enlace = 0
        hashtags = 0 
        

        marker = folium.Marker(location=[float(latitude), float(longitude)]) 
        popup_html = f'''
        <div style="position: relative; display: inline-block; min-width: 125px ;padding: 5px; background-color: 
        rgba(255, 255, 255, 0.8); border: 2px solid black; border-radius: 
        5px; font-family: Arial; font-size: 12pt;">
        @<b>{usuario}:</b>\n
        {message}\n\n
        {enlace}\n\n
        {hashtags}\n\n
        <i>{fechayhora}:</i>
        <i>IDDB:{dbid}</i>
        </div>
        '''
        popup = folium.Popup(html=popup_html, max_width=250)

        # Asociar el popup al marcador
        marker.add_child(popup)

        # Añadir el marcador al mapa
        marker.add_to(map_osm)


        """icono = folium.features.DivIcon(
            
        html = f'''<div style="position: relative; display: inline-block; min-width: 125px ;padding: 5px; background-color: 
        rgba(255, 255, 255, 0.8); border: 2px solid black; border-radius: 
        5px; font-family: Arial; font-size: 12pt;">
        @<b>{usuario}:</b>\n
        {message}\n\n
        {enlace}\n\n
        {hashtags}\n\n
        <i>{fecha}:</i>
        <i>{hora}</i>
        
        </div>'''
        )"""
        #folium.Marker(location=[latitude, longitude],icon=icono).add_to(map_osm)
        #folium.Marker(location=[float(latitude), float(longitude)]).add_to(map_osm)
        map_osm.save('teleport_app/templates/map/index.html')
    
    
#cargar_marcadores_desde_db()


    
   
