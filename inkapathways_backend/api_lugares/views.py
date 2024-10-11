from rest_framework import generics
from .models import TablalugaresV2
from .serializers import Serializer_lugares_v2



class getLugaresTuristicos(generics.ListAPIView):
    queryset = TablalugaresV2.objects.all()
    serializer_class = Serializer_lugares_v2
