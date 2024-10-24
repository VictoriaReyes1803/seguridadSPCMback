
from io import BytesIO
import logging
import os
import boto3
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from ..models import  Producto, Producto_maquina, Maquina, Reporte
from ..serializers import  ProductoSerializer, MaquinaSerializer, ProductoMaquinaSerializer, ReporteSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousFileOperation
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class Productos(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Producto.objects.filter(estado=True)  
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProductoMaquina(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = ProductoMaquinaSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, producto , *args, **kwargs):
        producto_maquina_obj = get_object_or_404(Producto_maquina, Ruta=producto)

        if producto_maquina_obj:
            serializer = ProductoMaquinaSerializer(producto_maquina_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
class Maquinaget(generics.ListAPIView):
    queryset = Maquina.objects.filter(estado=True)  
    serializer_class = MaquinaSerializer
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        maquinas = self.get_queryset()
        serializer = self.get_serializer(maquinas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReporteView(generics.ListCreateAPIView):
    # view de post de reportes
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Reporte.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self,  request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
    
class AllReportsView(generics.ListAPIView):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]

class ReporteDetailView(generics.RetrieveUpdateDestroyAPIView):
      # view de reportes get por usuario ID
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reporte.objects.filter(user=self.request.user)
    

class UploadPDFView(generics.ListCreateAPIView):
        def post(self, request, *args, **kwargs):
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({'error': 'No file provided'}, status=400)
            try:
                file_name = uploaded_file.name
                file_content = uploaded_file.read()
                session = boto3.session.Session()
                client = session.client('s3',
                                        region_name=settings.SPACES_REGION,
                                        endpoint_url=settings.SPACES_ENDPOINT_URL,
                                        aws_access_key_id=settings.SPACES_ACCESS_KEY_ID,
                                        aws_secret_access_key=settings.SPACES_SECRET_ACCESS_KEY)
                
                client.upload_fileobj(BytesIO(file_content), settings.SPACES_BUCKET_NAME, file_name, ExtraArgs={
                    'ContentType': 'application/pdf',
                    'ContentDisposition': 'inline',
                    'ACL': 'public-read'  # Esto asegura que el archivo sea público
                })
                file_url = f"https://nyc3.digitaloceanspaces.com/clayenss/{settings.SPACES_BUCKET_NAME}/{file_name}"
                print(file_url)

                return Response( {'file_url': file_url}
                    , status=status.HTTP_201_CREATED)
            
            except NoCredentialsError:
                return Response({'error': 'Credentials not available'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListPDFView(APIView):
    #get de los pdf en digital
    def get(self, request, *args, **kwargs):
        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    region_name=settings.SPACES_REGION,
                                    endpoint_url='https://nyc3.digitaloceanspaces.com',
                                    aws_access_key_id=settings.SPACES_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.SPACES_SECRET_ACCESS_KEY,
                                    config=boto3.session.Config(s3={'addressing_style': 'path'}))
            
            
            print(f"Listando objetos en el bucket: {settings.SPACES_BUCKET_NAME}")
            response = client.list_objects_v2(Bucket='clayenss')
            print(f"Respuesta de list_objects_v2: {response}")
            if 'Contents' in response:
                pdf_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.pdf')]
            else:
                pdf_files = []
                
            

            return Response({'pdf_files': pdf_files}, status=status.HTTP_200_OK)
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"ClientError: {error_code} - {error_message}")
            return Response({'error': f'Client error {error_code}: {error_message}'}, status=status.HTTP_400_BAD_REQUEST)
        
        except (NoCredentialsError, PartialCredentialsError):
            return Response({'error': 'Credentials not available or incomplete'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)