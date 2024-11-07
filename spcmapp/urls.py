from django.urls import path
from django.conf import settings
from .views.views import Productos, ProductoMaquina, Maquinaget, ReporteView, ReporteDetailView, UploadPDFView, ListPDFView, AllReportsView, UpdatePDFView, DeletePDFView
from .views.auth_views import RegisterView, LoginView, UserProfileView ,LogoutView, SendRecoveryEmailView, ResetPasswordView, reset_password_view
from .views.user_views import user_views
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('productos/', Productos.as_view(), name='productos'),
    path('producto-maquina/<str:producto>/', ProductoMaquina.as_view(), name='producto_maquina_detail'),
    path('maquinas/', Maquinaget.as_view(), name='maquina-list'),
    path('reportes/', ReporteView.as_view(), name='reportes'),# get por user logueado y post de reporte
    path('reportes/<int:pk>/', ReporteDetailView.as_view(), name='reporte-detail-update-delete'),#put y delete por id de reporte
    path('all-report/', AllReportsView.as_view(), name='all-reports'),
    path('reportes/<int:user_id>/<int:pk>/', ReporteDetailView.as_view(), name='reporte-detail'), # get por id de reporte
    path('pdf/', UploadPDFView.as_view(), name='pdf'),# pdf en digital
    path('pdfs/', ListPDFView.as_view(), name='pdfs'),
    path('update/', UpdatePDFView.as_view(), name='update-pdf'),
    path('pdf/delete/<int:id_report>/', DeletePDFView.as_view(), name='delete-pdf'),
    
    
    path('users/', user_views.get_users, name='get_users'),
    path('users/<int:user_id>/', user_views.get_user, name='get_user'),
    path('users/create/', user_views.create_user, name='create_user'),
    path('users/update/<int:user_id>/', user_views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', user_views.delete_user, name='delete_user'),


    path('send-email/', SendRecoveryEmailView.as_view(), name='send-recovery-email'),
    path('api/reset-password/<uidb64>/<token>/', reset_password_view, name='reset-password'),
    path('api/api/reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='api-reset-password'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

