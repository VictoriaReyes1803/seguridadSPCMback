
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Email: {email}, Password: {password}")
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
