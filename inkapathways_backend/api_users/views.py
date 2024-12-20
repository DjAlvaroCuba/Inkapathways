from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Usuario
from .serializers import UsuarioSerializer, EmptySerializer , UsuarioLoginSerializer
from django.contrib.auth.hashers import make_password, check_password
import secrets  # Para generar un token único
from api_users.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView


class RegistroUsuarioView(GenericAPIView):
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Hashear la contraseña antes de guardarla
            serializer.validated_data['contraseña_hash'] = make_password(
                serializer.validated_data['contraseña_hash'])
            usuario = serializer.save()

            # Generar un token de verificación único
            token_verificacion = secrets.token_urlsafe(32)
            usuario.fecha_expiracion_token = timezone.now() + timedelta(hours=1)

            # Guardar el token de verificación en el usuario
            usuario.token_verificacion = token_verificacion
            usuario.save()

            return Response({
                'token_verificacion': token_verificacion,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUsuarioView(GenericAPIView):  # Mantener GenericAPIView
    # Usar UsuarioSerializer para validar el correo
    serializer_class = UsuarioLoginSerializer

    def post(self, request, *args, **kwargs):
        # Solo extraer el correo y contraseña del request
        correo = request.data.get('correo')
        contraseña = request.data.get('contraseña_hash')

        # Validar que el correo y la contraseña estén presentes
        if not correo or not contraseña:
            return Response({'error': 'Correo y contraseña son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar la contraseña
        if check_password(contraseña, usuario.contraseña_hash):
            # Generar un nuevo token de verificación
            token_verificacion = secrets.token_urlsafe(32)
            # Actualiza el token de verificación
            usuario.token_verificacion = token_verificacion
            usuario.fecha_expiracion_token = timezone.now() + timedelta(hours=1)
            usuario.save()

            return Response({
                'token_verificacion': token_verificacion,
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutUsuarioView(GenericAPIView):
    # Puedes mantener GenericAPIView o usar APIView
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response({'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        # Dividir el header en partes para evitar errores de índice
        parts = auth_header.split()

        # Verificar que el formato del token sea 'Bearer <token>' o solo '<token>'
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token_verificacion = parts[1]  # Caso 'Bearer token'
        elif len(parts) == 1:
            token_verificacion = parts[0]  # Caso solo 'token'
        else:
            return Response({'error': 'Formato de token inválido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(
                token_verificacion=token_verificacion)

            # Invalida el token de verificación
            usuario.token_verificacion = None
            usuario.save()

            return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'error': 'Token inválido. Inicie sesión de nuevo.'}, status=status.HTTP_400_BAD_REQUEST)


class VistaProtegidaView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        usuario = request.user  # Obtener el usuario autenticado

        # Verificar si el token ha expirado
        if usuario.fecha_expiracion_token and usuario.fecha_expiracion_token < timezone.now():
            return Response({'error': 'El token ha expirado, por favor inicie sesión nuevamente.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'message': 'Accediste a una ruta protegida'}, status=status.HTTP_200_OK)
