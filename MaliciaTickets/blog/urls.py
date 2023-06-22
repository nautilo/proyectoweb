from django.urls import path, include
from . import views

urlpatterns = [   
    # Aquí la ruta localhost:8000 hace llamado a una
    path('', views.noticias),

    # localhost:8000/noticia/1
    path('noticia/<int:pk>/', views.noticia, name='noticia'),
    path('noticia/new',views.nueva_noticia,name='nueva_noticia'),
    path('noticia/<int:pk>/editar/',views.editar_noticia,name='editar_noticia'),
]