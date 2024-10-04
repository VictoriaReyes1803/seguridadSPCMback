
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from .models import User , producto_maquina, Producto
from .serializers import UserSerializer, ProductoSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Email: {email}, Password: {password}")
        
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

class Productos(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]  
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)