
from rest_framework.generics import ListAPIView
from api_users.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Festividad
from .serializers import FestividadSerializer


class FestividadListView(ListAPIView):
    queryset = Festividad.objects.all()  
    serializer_class = FestividadSerializer  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]