from django import forms
from .models import Evento
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

    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, widget=forms.RadioSelect,label="Tipo de usuario:")
    biografia = forms.CharField(max_length=1000,required=False)
    class Meta:
        model = User
        fields = ["username","first_name","email","password1","password2","tipo_usuario","biografia"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("biografia")
class UserUpdateForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('1', 'Productor/a'),
        ('2', 'Artista'),
    ]
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, widget=forms.RadioSelect,label="Tipo de usuario:")
    imagen = forms.ImageField(label="Imagen de perfil", required=False)
    biografia = forms.CharField(max_length=1000,required=False,widget=forms.Textarea)
    class Meta:
        model = User
        fields = ["imagen","first_name","tipo_usuario","biografia"]