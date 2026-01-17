from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.auth_login, name='login'),

    path('', views.home_page, name='home_page'),
    path('booking/', views.booking, name='booking'),
    path('confirm/<int:order_id>/', views.conform_order, name='conform_order'),
    path('about/', views.about, name='about'),
    
] 
