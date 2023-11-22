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
    imagen = models.ImageField(upload_to='static/img/eventos/', blank=True, default='static/img/eventos/default.png')
    
    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    OPCIONES_TIPO_USUARIO = [
        ('1', 'Cliente'),
        ('2', 'Empleado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    first_name = models.CharField(max_length=30, blank=True)
    biografia = models.TextField(blank=True)
    tipo_perfil = models.CharField(max_length=1, choices=OPCIONES_TIPO_USUARIO)
    imagen_perfil = models.ImageField(upload_to='static/img/perfiles', blank=True, default='static/img/perfiles/default.png')

    def __str__(self):
        return self.user.username
