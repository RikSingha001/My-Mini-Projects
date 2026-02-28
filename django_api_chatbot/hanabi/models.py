from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.conf import settings
# Create your models here.
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

# class Ai_Assistant(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     message = models.TextField()
#     response = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user} - {self.timestamp}"
    
class ChatRequest(models.Model):
    message = models.TextField()

class ChatResponse(models.Model):
    request = models.ForeignKey(ChatRequest, on_delete=models.CASCADE)
    reply_main = models.TextField()
    reply_secondary = models.TextField()

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
