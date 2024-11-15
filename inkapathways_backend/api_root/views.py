from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Pregunta, Respuesta
from .serializers import PreguntaSerializer, RespuestaSerializer
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

        