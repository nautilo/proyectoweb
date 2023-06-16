from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

class Perfil(models.Model):
    OPCIONES_TIPO_USUARIO = [
        ('1', 'Productor/a'),
        ('2', 'Artista'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.CharField(max_length=1000, blank=True)
    tipo_perfil = models.CharField(max_length=1, choices=OPCIONES_TIPO_USUARIO)
    imagen_perfil = models.ImageField(upload_to='perfiles', blank=True)

    def __str__(self):
        return self.usuario.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(usuario=instance)