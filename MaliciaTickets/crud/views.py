from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, EventoForm, PerfilForm
from .models import Evento, Perfil
from django.contrib.auth.models import User
from crud.models import Perfil
from blog.models import Post


def ingresar(view_func):
    def wrapper(request, *args, **kwargs):
        form_registro = RegistroForm()
        form_login = AuthenticationForm(request, data=request.POST)

        if request.method == 'POST':
            form_registro = RegistroForm(data=request.POST)
            if form_registro.is_valid():
                user = form_registro.save()
                perfil = user.perfil
                perfil.first_name = user.first_name
                perfil.save()
                user = authenticate(username=form_registro.cleaned_data["username"], password=form_registro.cleaned_data["password1"])
                login(request, user)
                return redirect('home')

            if form_login.is_valid():
                username = form_login.cleaned_data.get('username')
                password = form_login.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return mostrar_perfil(request,user.username)
                else:
                    messages.error(request, 'La autenticación falló.')
        else:
            form_login = AuthenticationForm(request)

        context = {
            'form_registro': form_registro,
            'form_login': form_login
        }

        return view_func(request, *args, **kwargs, **context)

    return wrapper

def buscar_eventos(request):
    texto_busqueda = request.GET.get('txtBuscar', '')
    eventos = Evento.objects.filter(nombre__icontains=texto_busqueda)
    context = {
        'eventos': eventos,
        'texto_busqueda': texto_busqueda,
    }
    return render(request, 'index.html', context)

@ingresar
def home(request, form_registro, form_login):
    # Verificar si el superusuario ya tiene un perfil asignado
    superusuario = User.objects.filter(username='maliciatickets').first()
    perfil_superusuario, creado = Perfil.objects.get_or_create(user=superusuario)
    # Guardar el perfil
    perfil_superusuario.save()
    
    posts = Post.objects.all()
    return render(request, 'index.html', {'form_registro': form_registro, 'form_login': form_login,'posts':posts})

def noticias(request):
    posts = Post.objects.all()
    return render(request, 'blog/noticias.html', {'posts': posts})



@ingresar
def explorar(request, form_registro, form_login):
    return render(request, 'paginas/explorar.html', {'form_registro': form_registro, 'form_login': form_login})


@ingresar
def acerca_de(request, form_registro, form_login):
    return render(request, 'paginas/acerca_de.html', {'form_registro': form_registro, 'form_login': form_login})


@ingresar
def contacto(request, form_registro, form_login):
    return render(request, 'paginas/contacto.html', {'form_registro': form_registro, 'form_login': form_login})

def logout_view(request):
    logout(request)
    return redirect('home')


def mostrar_perfil(request, username):
    user = get_object_or_404(User, username=username)
    perfil = user.perfil
    eventos = Evento.objects.filter(user=user)
    return render(request, 'crud/perfil.html', {'eventos': eventos, 'perfil': perfil})

@login_required
def editar_perfil(request):
    perfil = get_object_or_404(Perfil, user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return mostrar_perfil(request,perfil.user.username)
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'crud/editar_perfil.html', {'form': form})
def evento(request,id):
    evento = get_object_or_404(Evento, id=id)
    return render(request,'crud/evento.html',{'evento':evento})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.user = request.user  # Set authenticated user as the value for the 'user' field
            evento.save()
            messages.success(request, '¡Tu evento ya está publicado!', 'Felicitaciones')
            return mostrar_perfil(request,evento.user.username)
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
            return mostrar_perfil(request,evento.user.username)
    else:
        form = EventoForm(instance=evento)
    return render(request, 'crud/editar_evento.html', {'form': form, 'evento': evento})


@login_required
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado correctamente.', 'Eliminado')
        return mostrar_perfil(request,evento.user.username)
    return render(request, 'crud/eliminar_evento.html', {'evento': evento})
