# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Usuario
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Obtener el token de acceso de los headers
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # Si no se provee un token, no autenticamos

        # Dividir el header en partes para evitar errores de índice
        parts = auth_header.split()

        # Verificar que el formato del token sea 'Bearer <token>' o solo '<token>'
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token_verificacion = parts[1]  # Caso 'Bearer token'
        elif len(parts) == 1:
            token_verificacion = parts[0]  # Caso solo 'token'
        else:
            return None  # Formato incorrecto

        try:
            # Buscamos al usuario en la base de datos con el token de acceso
            usuario = Usuario.objects.get(
                token_verificacion=token_verificacion)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Token inválido, iniciar sesion')

        # Retornar el usuario y None (DRF requiere una tupla de (usuario, auth))
        return (usuario, None)
    
class CustomTokenAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'api_users.authentication.TokenAuthentication'  # El path a tu clase
    name = 'CustomTokenAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        }
