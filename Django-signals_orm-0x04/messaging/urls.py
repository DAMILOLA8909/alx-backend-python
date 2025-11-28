from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.home, name='home'),
    path('delete-account/', views.delete_user_account, name='delete_account'),
    # New threaded conversation URLs
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:user_id>/', views.conversation_detail, name='conversation_detail'),
    path('thread/<int:message_id>/', views.message_thread, name='message_thread'),
    path('reply/<int:message_id>/', views.reply_to_message, name='reply_to_message'),
]