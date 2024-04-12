import re, os
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

def separar_mensaje(message):

    texto = message
            # Expresión regular para encontrar el enlace y los hashtags
    pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|#\w+'
    patternhash = r'#\w+'
    parts = re.split(pattern, texto)
    mensaje = parts[0]
    if len(parts) == 1:
        mensaje = parts[0]
        enlace = ""
    else:
        mensaje = parts[0]
        enlace = parts[1]

    if enlace == None or enlace == "":
        enlace = ""
    hashtags = re.findall(patternhash, texto)
# Solo conservar los tres primeros hashtags
    hashtags = hashtags[:3]
    hashtags_str = ' '.join(hashtags)

    mensaje = mensaje.replace('\n', ' ')  # Reemplaza \n con un espacio
    # Define el tipo por defecto
    tipo = "general"

    # Busca los comandos en el texto y asigna el tipo correspondiente
    if "--%e" in texto:
        tipo = "evento"
    elif "--%v" in texto:
        tipo = "venta"
    elif "--%i" in texto:
        tipo = "informacion"
    elif "--%a" in texto:
        tipo = "alerta"



    return mensaje, enlace, hashtags_str, tipo

