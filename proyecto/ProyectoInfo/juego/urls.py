from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_preguntas, name='listar_preguntas'),
    path('/crear', views.crear_pregunta, name='crear_pregunta'),
]

#    path('crear', views.crear_juego, name='crear_juego'),
#   path('detalle/<int:identificador>', views.detalle_juego, name='detalle_juego'),

