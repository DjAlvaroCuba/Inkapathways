from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Pregunta, Respuesta
from .serializers import PreguntaSerializer, RespuestaSerializer
from api_users.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class PreguntaList(APIView):
    def get(self, request):
        preguntas = Pregunta.objects.all()
        serializer = PreguntaSerializer(preguntas, many=True)
        return Response(serializer.data)

class RespuestaList(APIView):
    def get(self, request):
        respuestas = Respuesta.objects.all()
        serializer = RespuestaSerializer(respuestas, many=True)
        return Response(serializer.data)
    
class TripticoFinal(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        # Filtrar respuestas que pertenezcan al usuario autenticado
        respuestas = Respuesta.objects.filter(usuario=usuario)
        serializer = RespuestaSerializer(respuestas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
