from django.urls import path
from .views import PreguntaList, RespuestaList, TripticoFinal
urlpatterns = [
    path('preguntas/', PreguntaList.as_view(), name='pregunta-list'),
    path('respuestas/', RespuestaList.as_view(), name='respuesta-list'),
    path('triptico/', TripticoFinal.as_view(), name="triptico")
]
