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
from django.views.decorators.csrf import csrf_exempt
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions

#https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
#https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
#https://www.transbankdevelopers.cl/referencia/webpay

# Tipo de tarjeta   Detalle                        Resultado
#----------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)


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
    posts = Post.objects.all()
    texto_busqueda = request.GET.get('txtBuscar', '')
    eventos = Evento.objects.filter(nombre__icontains=texto_busqueda)
    context = {
        'eventos': eventos,
        'texto_busqueda': texto_busqueda,
        'posts':posts,
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


@csrf_exempt
def iniciar_pago(request,id):
    evento = get_object_or_404(Evento, id=id)
    return_url = 'http://127.0.0.1:8000/pago_exitoso/'+str(id)
    commercecode = '597055555532'
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
    if request.method == 'POST':
        cliente = "cliente"
        email = "email"
        cantidadentradas=request.POST.get('cantidadentradas')
        monto = str(int(cantidadentradas)*evento.precio)

        buy_order = evento.nombre[0:26]
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.create(buy_order, cliente, monto, return_url)

        context = {
            "buy_order": buy_order,
            "session_id": cliente,
            "amount": monto,
            "return_url": return_url,
            "response": response,
            "token_ws": response['token'],
            "url_tbk": response['url'],
            "email": email,
            "cantidadentradas":cantidadentradas,
            "preciounitario":int(monto)//int(cantidadentradas)
        }
        return render(request, 'crud/iniciar_pago.html', context)
    return evento(request,id)

@csrf_exempt
def pago_exitoso(request,id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))
        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.commit(token=token)
        print("response: {}".format(response))

        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": "nombre",
            "last_name": "apellido",
            "email": "email",
            "rut": "11.111.111-K",
            "direccion": "Calle Falsa #123",
            "response_code": response['response_code'],
            "evento":evento,
        }
        evento.entradas_disponibles = evento.entradas_disponibles - int(context['amount'])//evento.precio
        evento.save()
        return render(request, "crud/pago_exitoso.html", context)
    else:
        return evento(request,id)