from django import forms
from django.contrib.auth.models import User
from .models import Evento, Perfil

class UsuarioEdicionForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    biografia = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']

        # Actualizar el perfil asociado al usuario
        perfil = Perfil.objects.get(user=user)
        perfil.first_name = self.cleaned_data['first_name']
        perfil.biografia = self.cleaned_data['biografia']
        perfil.save()

        if commit:
            user.save()

        return user

class RegistroForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    tipo_perfil = forms.ChoiceField(choices=Perfil.OPCIONES_TIPO_USUARIO, widget=forms.RadioSelect)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
            perfil = Perfil.objects.create(user=user, first_name=user.first_name, tipo_perfil=self.cleaned_data['tipo_perfil'])
        return user


class PerfilForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(choices=Perfil.OPCIONES_TIPO_USUARIO, widget=forms.RadioSelect)

    class Meta:
        model = Perfil
        fields = ['first_name', 'biografia', 'tipo_usuario', 'imagen_perfil']



class EventoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EventoForm, self).__init__(*args, **kwargs)
        if user and not self.instance.pk:
            self.initial['username'] = user.username
        self.fields['imagen'].required = False

    class Meta:
        model = Evento
        exclude = ['user']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
        }
