from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contraseña_hash', 'lugar_procedencia']
        extra_kwargs = {'contraseña_hash': {'write_only': True}}
        
class EmptySerializer(serializers.Serializer):
    
    pass

class UsuarioLoginSerializer(serializers.Serializer):
    correo = serializers.EmailField(required=True)
    contraseña_hash = serializers.CharField(required=True, write_only=True)