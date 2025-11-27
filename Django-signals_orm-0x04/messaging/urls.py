from django.urls import path
from . import views

app_name = 'messaging'  # Keep the namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('delete-account/', views.delete_user_account, name='delete_account'),
]