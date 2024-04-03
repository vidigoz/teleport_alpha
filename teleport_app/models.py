from django.db import models
from django.db.models.fields import CharField, FloatField, TextField

class TeleportDatabase(models.Model):
    message = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    fecha = models.TextField()
    hora = models.TextField()
    usuario = models.TextField()
    userid = models.TextField()
    show = models.BooleanField(default=True)
    


  
    
 # Create your models here.
