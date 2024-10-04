# middleware.py

from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header:
            try:
                # Extraer el token de la cabecera
                token = auth_header.split()[1]  # Suponiendo 'Bearer <token>'
                # Verificar el token
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                request.user = jwt_auth.get_user(validated_token)  # Asignar el usuario a la solicitud
            except (AuthenticationFailed, IndexError):
                return JsonResponse({'detail': 'Token inválido o no proporcionado.'}, status=403)

        response = self.get_response(request)
        return response