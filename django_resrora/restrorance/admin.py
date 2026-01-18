from django.contrib import admin
from .models import RoomType, Booking, Review, Profile

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_rooms')
    list_editable = ('total_rooms',)  # এখানে সরাসরি total_rooms update করা যাবে
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_type', 'check_in', 'check_out', 'status')
    list_filter = ('room_type', 'status')
    search_fields = ('user__username',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')
