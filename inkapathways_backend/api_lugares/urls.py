from django.urls import path
from .views import getLugaresTuristicos


urlpatterns = [
    path('v2/', getLugaresTuristicos.as_view(), name='tu_modelo_list'),  
    
]