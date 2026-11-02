import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    


class Hospital(models.Model):

    SERVICE_TYPES = (
        ('Heart Attack', 'Heart Attack'),
        ('Pregnancy', 'Pregnancy'),
        ('Accident', 'Accident'),
        ('All', 'All'),
    )

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    address = models.TextField()

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPES
    )

    ambulance_count = models.IntegerField(default=1)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"
    
class EmergencyRequest(models.Model):

    EMERGENCY_TYPES = (
        ('Heart Attack', 'Heart Attack'),
        ('Pregnancy', 'Pregnancy'),
        ('Accident', 'Accident'),
        ('All', 'All'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    state = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    full_address = models.CharField(max_length=255)

    emergency_type = models.CharField(
        max_length=50,
        choices=EMERGENCY_TYPES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    assigned_hospital = models.ForeignKey(
        'Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.phone_number} - {self.emergency_type}"
    
class Hospital_registration(models.Model):
   
   # hospital name, hospital address, phone number, service type, ambuleance key code
   hospital_name = models.CharField(max_length=200)
   hospital_address = models.TextField()
   hospital_phone = models.CharField(max_length=20)
   
   ambulance_key_code = models.CharField(
        max_length=20,
        unique=True
    )
   def __str__(self):
            return self.hospital_name
#    def save(self, *args, **kwargs):

#         if not self.ambulance_key_code:

#             self.ambulance_key_code = str(uuid.uuid4())[:8].upper()

#         super().save(*args, **kwargs)
        # def __str__(self):
        #     return self.hospital_name
    


class ambulance_driver_registration(models.Model):

    hospital = models.ForeignKey(
        Hospital_registration,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    SERVICE_TYPES = (
        ('Heart Attack', 'Heart Attack'),
        ('Pregnancy', 'Pregnancy'),
        ('Accident', 'Accident'),
        ('All', 'All'),
    )

    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    ambulance_number = models.CharField(max_length=20)

    ambulance_key_code = models.CharField(max_length=20)
    ambulance_service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPES
    )
    def __str__(self):
        return self.name
    

class ambulance_login(models.Model):

    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.phone





    
class Duty_onOff_modes(models.Model):

    ambulance_driver = models.ForeignKey(
    ambulance_driver_registration,
    on_delete=models.CASCADE,
    related_name="duty_status"
)

    is_on_duty = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ambulance_driver.name}"
    


class MatchedAmbulance(models.Model):

    emergency_request = models.ForeignKey(
        EmergencyRequest,
        on_delete=models.CASCADE
    )

    ambulance_driver = models.ForeignKey(
        ambulance_driver_registration,
        on_delete=models.CASCADE
    )

    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emergency_request} - {self.ambulance_driver}"