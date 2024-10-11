from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contraseña_hash', 'region']
        extra_kwargs = {'contraseña_hash': {'write_only': True}}
        
class EmptySerializer(serializers.Serializer):
    
    pass