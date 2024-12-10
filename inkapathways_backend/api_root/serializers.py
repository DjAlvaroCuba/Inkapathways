from rest_framework import serializers
from .models import Pregunta, Respuesta , Tripticos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

class TripticosSerializer(serializers.ModelSerializer):
    # Usar RespuestaSerializer para incluir detalles completos de las respuestas en la salida
    comidas = RespuestaSerializer(many=True, read_only=True)

    # Usar PrimaryKeyRelatedField para permitir enviar solo los IDs al crear/actualizar
    comidas_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Respuesta.objects.all(),
        write_only=True
    )

    class Meta:
        model = Tripticos
        fields = '__all__'  # Incluye todos los campos
        extra_kwargs = {
            'usuario': {'required': False},  # Opcional si el usuario se asigna automáticamente
        }

    def create(self, validated_data):
        comidas_ids = validated_data.pop('comidas_ids', [])
        triptico = Tripticos.objects.create(**validated_data)
        triptico.comidas.set(comidas_ids)  # Asocia las respuestas seleccionadas
        return triptico

    def update(self, instance, validated_data):
        comidas_ids = validated_data.pop('comidas_ids', None)
        if comidas_ids is not None:
            instance.comidas.set(comidas_ids)  # Actualiza las relaciones de comidas
        return super().update(instance, validated_data)
    
