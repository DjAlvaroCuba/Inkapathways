from rest_framework.response import Response
from rest_framework import status
from api_users.models import Usuario
from rest_framework.generics import GenericAPIView
from api_users.serializers import EmptySerializer
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from api_users.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import json
from django.utils import timezone
from .questions import generate_question

class WelcomeView(GenericAPIView):

    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        # Extrae el encabezado Authorization
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response({'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        # Dividir el encabezado en partes para obtener el token
        parts = auth_header.split()

        # Verificar que el formato del token sea 'Bearer <token>' o solo '<token>'
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token_verificacion = parts[1]  # Caso 'Bearer token'
        elif len(parts) == 1:
            token_verificacion = parts[0]  # Caso solo 'token'
        else:
            return Response({'error': 'Formato de token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        # Busca al usuario que tenga el token
        try:
            usuario = Usuario.objects.get(token_verificacion=token_verificacion)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Si el token es válido, responde con el mensaje de bienvenida
        return Response({
            "message": f"Hola {usuario.nombre}, bienvenido a Inkapathways!",
            "credenciales": {
                "correo": usuario.correo,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "region": usuario.region
            }
        }, status=status.HTTP_200_OK)
    

class QuestionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user  # Obtener el usuario autenticado

        # Verificar si el token ha expirado
        if usuario.fecha_expiracion_token and usuario.fecha_expiracion_token < timezone.now():
            return Response({'error': 'El token ha expirado, por favor inicie sesión nuevamente.'}, status=status.HTTP_401_UNAUTHORIZED)

        previous_question = request.data.get('previous_question', '')
        previous_response = request.data.get('previous_response', '')

        # Generar la nueva pregunta
        question_data = generate_question(previous_question, previous_response)

        if question_data:
            return Response(question_data)
        
        return Response({"error": "No se pudo generar la pregunta"}, status=status.HTTP_400_BAD_REQUEST)