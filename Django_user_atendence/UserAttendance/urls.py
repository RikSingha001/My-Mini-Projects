from django.contrib import admin
from django.urls import path, include

from UserAttendance import views


urlpatterns = [
      path('attendance_sum/', views.attendance_sum, name='attendance_sum'),
    # path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("logout/", views.logout_view, name="logout"),
    path('attendance_history/', views.attendance_history, name='attendance_history'),
    path('profile/', views.profile, name='profile'),
    path('resign_application/', views.resign_application, name='resign_application'),
    path('login_logout_history/', views.login_logout_history, name='login_logout_history'),
    # path('leave_history/', views.leave_history, name='leave_history'),
    path('leave_application/', views.leave_application, name='leave_application'),
    path('attendance_out/', views.attendance_out, name='attendance_out'),
]