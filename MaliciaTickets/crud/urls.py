from django.urls import path
from . import views

urlpatterns=[
    path('',views.lista_eventos,name='lista_eventos'),
    path('crear/',views.crear_evento,name='crear_evento'),
    path('editar/<str:id>/',views.editar_evento,name='editar_evento'),
    path('eliminar/<str:id>/',views.eliminar_evento,name='eliminar_evento'),
]