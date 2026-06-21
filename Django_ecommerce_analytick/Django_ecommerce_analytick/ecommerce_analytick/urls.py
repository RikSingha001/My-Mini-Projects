from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from ecommerce_analytick import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),


]