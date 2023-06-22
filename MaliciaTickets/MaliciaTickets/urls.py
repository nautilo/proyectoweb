"""
URL configuration for MaliciaTickets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from crud.views import buscar_eventos, home, logout_view,explorar,acerca_de,contacto,mostrar_perfil,editar_perfil,evento,buscar_eventos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('explorar/',explorar,name='explorar'),
    path('acerca_de/',acerca_de,name='acerca_de'),
    path('contacto/',contacto,name='contacto'),
    path('perfil/',include('crud.urls')),
    path('editar_perfil/',editar_perfil,name='editar_perfil'),
    path('perfil/<str:username>/', mostrar_perfil, name='mostrar_perfil'),
    path('evento/<int:id>/',evento,name='evento'),
    path('buscar_eventos/', buscar_eventos, name='buscar_eventos'),
    path('noticias/',include('blog.urls')),
]
