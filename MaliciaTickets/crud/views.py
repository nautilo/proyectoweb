from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserCreationForm, EditarPerfilForm, EventoForm
from .models import Evento


def home(request):
    form_registro = CustomUserCreationForm()
    form_login = AuthenticationForm(request, data=request.POST)
    
    if request.method == 'POST':
        form_registro = CustomUserCreationForm(data=request.POST)
        if form_registro.is_valid():
            form_registro.save()
            user = authenticate(username=form_registro.cleaned_data["username"], password=form_registro.cleaned_data["password1"])
            messages.success(request, 'Te has registrado correctamente.', 'Bienvenidx')
            return redirect('home')
        
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('perfil')
            else:
                messages.error(request, 'La autenticación falló.')
        else:
            form_login = AuthenticationForm(request)
    
    return render(request, 'index.html', {'form_registro': form_registro, 'form_login': form_login})


def explorar(request):
    form_registro = CustomUserCreationForm()
    form_login = AuthenticationForm(request, data=request.POST)
    return render(request, 'paginas/explorar.html', {'form_registro': form_registro, 'form_login': form_login})


def acerca_de(request):
    form_registro = CustomUserCreationForm()
    form_login = AuthenticationForm(request, data=request.POST)
    return render(request, 'paginas/acerca_de.html', {'form_registro': form_registro, 'form_login': form_login})


def contacto(request):
    form_registro = CustomUserCreationForm()
    form_login = AuthenticationForm(request, data=request.POST)
    return render(request, 'paginas/contacto.html', {'form_registro': form_registro, 'form_login': form_login})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def perfil(request):
    eventos = Evento.objects.all()
    return render(request, 'crud/perfil.html', {'eventos':eventos})


@login_required
def editar_perfil(request):
    perfil = request.user.perfil  # Obtener el perfil asociado al usuario actual

    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirigir a la página de perfil después de guardar los cambios
    else:
        form = EditarPerfilForm(instance=perfil)

    return render(request, 'crud/editar_perfil.html', {'form': form})


@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.user = request.user  # Set authenticated user as the value for the 'user' field
            evento.save()
            messages.success(request, '¡Tu evento ya está publicado!', 'Felicitaciones')
            return redirect('perfil')
    else:
        form = EventoForm()
    return render(request, 'crud/crear_evento.html', {'form': form})


@login_required
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento modificado correctamente.', 'Modificado')
            return redirect('perfil')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'crud/editar_evento.html', {'form': form, 'evento': evento})


@login_required
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado correctamente.', 'Eliminado')
        return redirect('perfil')
    return render(request, 'crud/eliminar_evento.html', {'evento': evento})
