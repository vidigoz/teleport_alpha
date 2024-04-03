import folium
import requests
from teleport_app.models import TeleportDatabase

import json

def cargar_marcadores_desde_db():

    map_osm = folium.Map(location=[32.663334, -115.467781], zoom_start=3)
    # Conecta a la base de datos
    #response = requests.get('http://localhost:8000/obtener_mensaje/')
    si = 200
    if si == 200:
        #data = response.json()

        #print(data)
        #print(len(data))
        #print(data)
        objetos_db = TeleportDatabase.objects.all()
        for datos in objetos_db:

            userid = datos.userid
            usuario = datos.usuario
            message = datos.message
            latitude = str(datos.latitude)
            longitude = str(datos.longitude)
            fecha = datos.fecha
            hora = datos.hora
            dbid = datos.id

            enlace = 0
            hashtags = 0
            
            print(latitude)
            print(userid)
            print(longitude) 
            print(message)  
            

            marker = folium.Marker(location=[float(latitude), float(longitude)]) 
            popup_html = f'''
            <div style="position: relative; display: inline-block; min-width: 125px ;padding: 5px; background-color: 
            rgba(255, 255, 255, 0.8); border: 2px solid black; border-radius: 
            5px; font-family: Arial; font-size: 12pt;">
            @<b>{usuario}:</b>\n
            {message}\n\n
            {enlace}\n\n
            {hashtags}\n\n
            <i>{fecha}:</i>
            <i>{hora}</i>
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
        return objetos_db
    else:
        print("Failed to get data from the API.")
        return None
    
#cargar_marcadores_desde_db()


    
   
