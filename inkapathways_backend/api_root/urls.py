from django.urls import path
from .views import PreguntaList, RespuestaList, TripticoFinal , TripticoCreateAPIView ,TripticoDetailAPIView
urlpatterns = [
    path('preguntas/', PreguntaList.as_view(), name='pregunta-list'),
    path('respuestas/', RespuestaList.as_view(), name='respuesta-list'),
    path('prediccion/', TripticoFinal.as_view(), name="prediccion"),
    path('triptico/', TripticoCreateAPIView.as_view(), name="Triptico"),
    path('triptico/<int:pk>/', TripticoDetailAPIView.as_view(), name="triptico-detail")
]
