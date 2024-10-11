
#from django.contrib import admin
from django.urls import path , include
from drf_spectacular.views import SpectacularAPIView , SpectacularRedocView , SpectacularSwaggerView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api-lugares-turisticos/', include('api_lugares.urls')),
    path('api/', SpectacularAPIView.as_view(),name='schema'),
    path('',SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('doc/',SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/usuarios/', include('api_users.urls')),
 
]
