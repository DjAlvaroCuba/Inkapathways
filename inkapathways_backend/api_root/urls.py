from django.urls import path
from .views import PreguntaList, RespuestaList
urlpatterns = [
    path('preguntas/', PreguntaList.as_view(), name='pregunta-list'),
    path('respuestas/', RespuestaList.as_view(), name='respuesta-list'),
]
