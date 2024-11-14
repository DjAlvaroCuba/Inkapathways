from django.urls import path
from .views import FestividadListView


urlpatterns = [
    path('v1/', FestividadListView.as_view(), name='lista'),  
    
]