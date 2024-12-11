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
    # Incluye detalles completos de las respuestas asociadas en la salida
    comidas = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Tripticos
        exclude = ['usuario']  # Excluir explícitamente 'usuario' de los datos recibidos

    def validate(self, attrs):
        """Validar que las fechas sean coherentes."""
        if attrs['fecha_salida'] > attrs['fecha_retorno']:
            raise serializers.ValidationError("La fecha de salida no puede ser posterior a la fecha de retorno.")
        return attrs

    def create(self, validated_data):
        """Crear un nuevo Triptico asociando usuario y respuestas automáticamente."""
        user = self.context['request'].user  # Identificar usuario autenticado
        validated_data['usuario'] = user

        # Obtener las respuestas relacionadas con el usuario autenticado
        respuestas_usuario = Respuesta.objects.filter(usuario=user)

        # Crear el Triptico
        triptico = Tripticos.objects.create(**validated_data)

        # Asociar respuestas automáticamente
        triptico.comidas.set(respuestas_usuario)
        return triptico

    def update(self, instance, validated_data):
        """Actualizar el Triptico y asociar respuestas automáticamente."""
        user = self.context['request'].user  # Identificar usuario autenticado
        respuestas_usuario = Respuesta.objects.filter(usuario=user)

        # Asociar respuestas automáticamente
        instance.comidas.set(respuestas_usuario)
        return super().update(instance, validated_data)