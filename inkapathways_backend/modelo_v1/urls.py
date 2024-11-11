from django.urls import path
from .views import WelcomeView , SearchComidasAPIView ,PreguntasAPI

urlpatterns = [
    path('api/welcome/', WelcomeView.as_view(), name='welcome'),
    path('consulta-faiss/',SearchComidasAPIView.as_view(), name='consulta-faiss'),
    path('respuesta-ia/', PreguntasAPI.as_view(), name='respuesta_ia'),
]
