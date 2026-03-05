
from django.urls import path

from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:chat_id>/', views.chat_box, name='chat_box'),



    
] 
