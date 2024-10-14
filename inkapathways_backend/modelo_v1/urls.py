from django.urls import path
from .views import WelcomeView

urlpatterns = [
    path('api/welcome/', WelcomeView.as_view(), name='welcome'),
    path('generar-pregunta/', WelcomeView.as_view(), name='welcome'),
    path('enviar-respuesta/', WelcomeView.as_view(), name='welcome'),
    

]
