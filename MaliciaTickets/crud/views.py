from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from .forms import EventoForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'crud/lista_eventos.html', {'eventos': eventos})


def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu evento ya está publicado!")
            return redirect('lista_eventos')
    else:
        form = EventoForm()
        return render(request, 'crud/crear_evento.html', {'form': form})


def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento modificado correctamente.")
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'crud/editar_evento.html', {'form': form, 'evento': evento})


def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, "Evento eliminado correctamente.")
        return redirect('lista_eventos')
    return render(request, 'crud/eliminar_evento.html', {'evento': evento})
