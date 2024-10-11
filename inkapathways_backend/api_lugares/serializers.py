from rest_framework import serializers
from .models import TablalugaresV2


class Serializer_lugares_v2(serializers.ModelSerializer):
    class Meta:
        model = TablalugaresV2
        fields = '__all__'
