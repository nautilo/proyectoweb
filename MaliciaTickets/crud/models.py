from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username',null=True)
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)
    precio = models.IntegerField()
    entradas_disponibles = models.IntegerField()
    descripcion = models.TextField(blank=True,null=True)
    imagen = models.ImageField(upload_to="eventos",null=True)
    
    def __str__(self):
        return self.name
