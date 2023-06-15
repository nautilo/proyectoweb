from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from .forms import EventoForm, CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

def home(request):
    form_registro = CustomUserCreationForm()
    form_login = AuthenticationForm(request,data=request.POST)
    if request.method == 'POST':
        form_registro = CustomUserCreationForm(data=request.POST)
        if form_registro.is_valid():
            form_registro.save()
            user = authenticate(username=form_registro.cleaned_data["username"],password=form_registro.cleaned_data["password1"])
            messages.success(request, {'title': 'Bienvenidx', 'message': 'Te has registrado correctamente.'})
            return redirect(to ="home")
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            
            # Autenticar al usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Iniciar sesión
                login(request, user)
                # Redireccionar a la página deseada
                return redirect('perfil')
            else:
                # Si la autenticación falla, mostrar un mensaje de error o realizar otra acción
                pass
        else:
            form_login = AuthenticationForm(request)
    return render(request,'index.html',{'form_registro':form_registro,'form_login':form_login})
def explorar(request):
    return render(request,'paginas/explorar.html')
def acerca_de(request):
    return render(request,'paginas/acerca_de.html')
def contacto(request):
    return render(request,'paginas/contacto.html')
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def perfil(request):
    eventos = Evento.objects.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST , request.FILES, instance= request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, {'title': 'Listo', 'message': 'Tu perfil ha sido actualizado.'})
            return redirect('perfil')
        else:
            messages.error(request, {'title': 'Error', 'message': 'No se pudo modificar el evento'})
    else:
        u_form = UserUpdateForm(instance = request.user)
        
    context = {
        'u_form': u_form,
        'eventos':eventos
    }
    
    return render(request,'crud/perfil.html', context)
@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.user = request.user  # Set authenticated user as the value for the 'user' field
            evento.save()
            messages.success(request, {'title': 'Felicitaciones', 'message': '¡Tu evento ya está publicado!'})
            return redirect('perfil')
    else:
        form = EventoForm()
    return render(request, 'crud/crear_evento.html', {'form': form})

def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, {'title': 'Modificado', 'message': 'Evento modificado correctamente.'})
            return redirect('perfil')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'crud/editar_evento.html', {'form': form, 'evento': evento})


def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, {'title': 'Eliminado', 'message': 'Evento eliminado correctamente.'})
        return redirect('perfil')
    return render(request, 'crud/eliminar_evento.html', {'evento': evento})