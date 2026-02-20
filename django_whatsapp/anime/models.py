from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, phone_number):
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number)
        user.set_unusable_password()   # 🔥 password disable
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        if not password:
            raise ValueError("Superuser must have a password")

        user = self.model(phone_number=phone_number)
        user.set_password(password)    # 🔐 admin এর জন্য password থাকবে
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

class LoginHistory(models.Model):
    phone_number = models.CharField(max_length=15)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.login_time}"

class search(models.Model):
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number
    
class ChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chats_user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chats_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.phone_number} - {self.user2.phone_number}"
    
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='chat_photos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.phone_number} Profile"

    
