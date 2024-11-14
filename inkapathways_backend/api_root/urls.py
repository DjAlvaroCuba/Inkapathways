from django.urls import path
from .views import UserAdminView
urlpatterns = [
    path('users/', UserAdminView.as_view(), name='usuarios'),
    
]
