from django import forms
from .models import Evento, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the 'user' argument from kwargs
        super(EventoForm, self).__init__(*args, **kwargs)
        if user and not self.instance.pk:  # Set the default value if user is authenticated and the instance is not being edited
            self.initial['username'] = user.username
        self.fields['imagen'].required = False
    class Meta:
        model = Evento
        exclude = ['user']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
        }


class CustomUserCreationForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('1', 'Productor/a'),
        ('2', 'Artista'),
    ]

    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, widget=forms.RadioSelect, label="Tipo de usuario:")

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2", "tipo_usuario"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil.objects.create(usuario=user)  # Crear el perfil asociado al usuario
        return user

class EditarPerfilForm(forms.ModelForm):
    OPCIONES_TIPO_USUARIO = [
        ('1', 'Productor/a'),
        ('2', 'Artista'),
    ]

    tipo_perfil = forms.ChoiceField(choices=OPCIONES_TIPO_USUARIO, widget=forms.RadioSelect, label="Tipo de perfil")

    class Meta:
        model = Perfil
        fields = ["biografia", "tipo_perfil", "imagen_perfil"]