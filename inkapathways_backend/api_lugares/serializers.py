from rest_framework import serializers
from .models import Festividad, Mes, Lugar

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = ['id', 'provincia']

class MesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mes
        fields = ['id', 'mes']

class FestividadSerializer(serializers.ModelSerializer):
    mes = MesSerializer()  # Relación con Mes
    lugar = LugarSerializer()  # Relación con Lugar

    class Meta:
        model = Festividad
        fields = ['id', 'nombre_festividad', 'descripcion_festividad', 'mes', 'lugar']
