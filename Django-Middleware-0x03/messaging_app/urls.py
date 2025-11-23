from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chats.auth import login_view, register_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Custom authentication URLs
    path('api/auth/login/', login_view, name='auth_login'),
    path('api/auth/register/', register_view, name='auth_register'),
    path('api/auth/logout/', logout_view, name='auth_logout'),
]