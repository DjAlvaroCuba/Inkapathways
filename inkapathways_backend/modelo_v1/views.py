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
    
class PruebaIAView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer
    def post(self, request, *args, **kwargs):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        version = 'models/gemini-1.5-flash'
        model = genai.GenerativeModel(version)
        datos_usuario = {
            "nombre": "Modelo entrenado de Alvaro",
            "intereses": "listo para resolver tus dudas y encontrar la mejor ruta de viaje a Junin"
        }
        prompt = f"Di lo siguiente: Hola soy el {datos_usuario['nombre']} y estoy {datos_usuario['intereses']}."

        try:
            # Generar contenido usando el modelo
            response = model.generate_content(prompt)
            # Retornar la respuesta como JSON
            return JsonResponse({'response': response.text})
        except Exception as e:
            # Manejo de excepciones
            return JsonResponse({'error': str(e)}, status=500)