from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User , producto_maquina, Producto
from .serializers import UserSerializer, ProductoSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        # print(f"Email: {email}, Password: {password}")
        
        user = None
        if email:
            user = authenticate(request, email=email, password=password)
        elif username:
            user = authenticate(request, username=username, password=password)


        if user is None:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Sesión cerrada correctamente'}, status=status.HTTP_205_RESET_CONTENT)
        except AttributeError as e:
            # Manejo específico de la excepción AttributeError
            return Response({'error': f'AttributeError: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Manejo general de otras excepciones
            return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
