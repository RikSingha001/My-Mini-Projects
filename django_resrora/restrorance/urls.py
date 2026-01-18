from django.urls import path

from . import views
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('review/', views.review, name='review'),
    path('all-reviews/', views.all_reviews, name='all_reviews'),  
    path('booking/', views.create_booking, name='booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('check-out/<int:booking_id>/', views.check_out, name='check_out'),
    path('adminsummary/', views.admin_summary, name='admin_summary'),
] 