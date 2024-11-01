from django.urls import path
from .views import WelcomeView , QuestionAPIView

urlpatterns = [
    path('api/welcome/', WelcomeView.as_view(), name='welcome'),
    path('generar-pregunta/',QuestionAPIView.as_view(), name='prueba_ia')
    #path('respuesta-ia/', RespuestaIAView.as_view(), name='respuesta_ia'),
]
