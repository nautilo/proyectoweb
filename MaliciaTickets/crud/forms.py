from django import forms
from .models import Evento
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class EventoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
        }

class CustomUserCreationForm(UserCreationForm):
    tipo_usuario = forms.CharField(max_length=1)
    class Meta:
        model = User
        fields = ["username","email","password1","password2","tipo_usuario"]
