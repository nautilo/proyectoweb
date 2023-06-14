from django.urls import path
from . import views

urlpatterns=[
    path('',views.lista_eventos,name='lista_eventos'),
    path('crear_evento/',views.crear_evento,name='crear_evento'),
    path('editar_evento/<int:id>/',views.editar_evento,name='editar_evento'),
    path('eliminar_evento/<int:id>/',views.eliminar_evento,name='eliminar_evento'),
]