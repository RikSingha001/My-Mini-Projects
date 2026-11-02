from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('hospital_registration/', views.registration_hospital, name='hospital_registration'),
    path('ambulance_registration/', views.ambulance_registration, name='ambulance_registration'),
    path('ambulance_login/', views.ambulance_login_view, name='ambulance_login_view'),
    path('ambulance_dashboard/', views.ambulance_dashboard, name='ambulance_dashboard'),
    path(
        'matched_ambulance/<int:hospital_id>/<int:emergency_id>/',
        views.matched_ambulance,
        name='matched_ambulance'
    ),
    
]