from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path("chat/<int:room_id>/", views.chat_room, name="chat_room"),
    path("profile/", views.profile_view, name="profile"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)