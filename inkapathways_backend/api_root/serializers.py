from rest_framework import serializers
from .models import Pregunta, Respuesta

# Serializador para Pregunta
class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = ['id', 'usuario', 'pregunta', 'fecha_creacion']

# Serializador para Respuesta
class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id', 'usuario', 'pregunta', 'respuesta', 'fecha_creacion']
