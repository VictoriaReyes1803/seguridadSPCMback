from django.urls import path

from .views.views import Productos, ProductoMaquina, Maquinaget, ReporteView, ReporteDetailView, UploadPDFView, ListPDFView, AllReportsView
from .views.auth_views import RegisterView, LoginView, LogoutView
from .views.user_views import user_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('productos/', Productos.as_view(), name='productos'),
    path('producto-maquina/<str:producto>/', ProductoMaquina.as_view(), name='producto_maquina_detail'),
    path('maquinas/', Maquinaget.as_view(), name='maquina-list'),
    path('reportes/', ReporteView.as_view(), name='reportes'),# get por user logueado y post de reporte
    path('all-report/', AllReportsView.as_view(), name='all-reports'),
    path('reportes/<int:pk>/', ReporteDetailView.as_view(), name='reporte-detail'),
    path('pdf/', UploadPDFView.as_view(), name='pdf'),# pdf en digital
    path('pdfs/', ListPDFView.as_view(), name='pdfs'),
    
    
    path('users/', user_views.get_users, name='get_users'),
    path('users/<int:user_id>/', user_views.get_user, name='get_user'),
    path('users/create/', user_views.create_user, name='create_user'),
    path('users/update/<int:user_id>/', user_views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', user_views.delete_user, name='delete_user'),
]