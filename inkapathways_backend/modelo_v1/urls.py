from django.urls import path
from .views import WelcomeView , SearchComidasAPIView

urlpatterns = [
    path('api/welcome/', WelcomeView.as_view(), name='welcome'),
    path('consulta-faiss/',SearchComidasAPIView.as_view(), name='consulta-faiss')
    #path('respuesta-ia/', RespuestaIAView.as_view(), name='respuesta_ia'),
]
