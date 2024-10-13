from rest_framework import generics
from .models import TablalugaresV2
from .serializers import Serializer_lugares_v2
from api_users.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class getLugaresTuristicos(generics.ListAPIView):
    queryset = TablalugaresV2.objects.filter(region='Junín')
    serializer_class = Serializer_lugares_v2
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
