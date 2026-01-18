from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username
class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    total_rooms = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
        ('CHECKED_OUT', 'Checked Out'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BOOKED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room_type} | {self.check_in} - {self.check_out}"


 
