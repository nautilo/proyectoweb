from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)
    precio = models.IntegerField()
    entradas_disponibles = models.IntegerField()
    descripcion = models.CharField(max_length=1000)
    imagen = models.ImageField(upload_to="eventos",null=True)
    
    def __str__(self):
        return self.name
