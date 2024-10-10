from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Producto

class AuthTests(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.productos_url = reverse('productos')
        
        
        self.user_data = {
            'email': 'usuario3@example.com',
            'nombre': 'Victoria',
            'username': 'Victoria.Reyes',
            'password': 'tu_contraseña_segura',
            'no_empleado': '123456',
            'apellido_paterno': 'Reyes',
            'apellido_materno': 'García',
            'rol': 'admin',
        }
        self.producto_data = {
            	'producto': '4023000201',
                'descripcion_1': 'CAP CLOSING CAP',
                'codigo_cliente': '40230-002-01',
                'resina_1': 'NORYL SE100X GRIS 780',
                'resina_2': 'NORYL SE100X GRIS 780',
                'categoria': 'PFA00',
                'Maquina': 'Máquina 1',
                'Estado': 'true'
        }

    def test_register(self):
        # Prueba de registro de usuario
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])

    def test_login(self):
        # Primero registramos un usuario
        self.client.post(self.register_url, self.user_data)
        
        # Prueba de inicio de sesión
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    def get_access_token(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        print(f'Token: {response.data["access"]}')  # Verifica si el token es correcto
        return response.data['access']

    def test_get_productos(self):
        self.client.post(self.register_url, self.user_data)
        
        login_response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.data['access']
        print(f'Token: {login_response}')  

        print(f'Token: {access_token}') 
        
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        print(headers)
        create_response = self.client.post(
            self.productos_url, 
            self.producto_data,
            **headers
            
        )
        
        print(f"Create response content: {create_response.json()}")  
        
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)  

        response = self.client.get(self.productos_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
