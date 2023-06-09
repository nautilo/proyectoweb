from django import forms
from .models import Evento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    tipo_usuario = forms.CharField(max_length=1)
    class Meta:
        model = User
        fields = ["username","email","password1","password2","tipo_usuario"]
