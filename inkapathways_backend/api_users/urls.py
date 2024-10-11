from django.urls import path
from .views import RegistroUsuarioView ,LogoutUsuarioView, VistaProtegidaView,LoginUsuarioView

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('login/', LoginUsuarioView.as_view(), name='login_usuario'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout_usuario'),
    path('protegida/', VistaProtegidaView.as_view(), name='vista_protegida'),

]
