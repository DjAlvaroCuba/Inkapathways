from rest_framework import serializers
from .models import TablalugaresV2


class Serializer_lugares_v2(serializers.ModelSerializer):
    class Meta:
        model = TablalugaresV2
        fields = [
            'id_lugar',
            'region', 
            'provincia',
            'distrito',
            'nombre_del_recurso',
            'categoria',
            'tipo_de_categoria',
            'sub_tipo_categoria'
        ]
