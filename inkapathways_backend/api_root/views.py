from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Pregunta, Respuesta , Tripticos
from .serializers import PreguntaSerializer, RespuestaSerializer , TripticosSerializer
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
    
class TripticoCreateAPIView(CreateAPIView):
    serializer_class = TripticosSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Incluye el contexto con la solicitud actual
        serializer = TripticosSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Guardar el nuevo Tríptico
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TripticoDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            triptico = Tripticos.objects.get(pk=pk)
        except Tripticos.DoesNotExist:
            return Response({"error": "Triptico no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TripticosSerializer(triptico)
        return Response(serializer.data, status=status.HTTP_200_OK)