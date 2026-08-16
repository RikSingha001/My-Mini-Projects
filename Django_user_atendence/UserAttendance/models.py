from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




def attendance_image_path(instance, filename):
    now = timezone.now()

    username = instance.user.username.replace(" ", "_")

    new_filename = (
        f"{username}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    )

    return new_filename

def attendance_out_image_path(instance, filename):

    now = timezone.now()

    username = instance.user.username.replace(" ", "_")

    new_filename = (
        f"{username}_OUT_"
        f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    )

    return new_filename


class Vendor(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    employee_name = models.CharField(
        max_length=150
    )

    mobile = models.CharField(
        max_length=15
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    status = models.CharField(
        max_length=50,
        default="Active"
    )

    def __str__(self):
        return f"{self.employee_id} - {self.employee_name}"




class UserAttendance(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    

    date = models.DateField(
        auto_now_add=True
    )

    time = models.TimeField(
        auto_now_add=True
    )

    image = models.ImageField(
        upload_to=attendance_image_path,
        blank=True,
        null=True
    )

    latitude = models.DecimalField(
    max_digits=12,
    decimal_places=7,
    null=True,
    blank=True
)

    longitude = models.DecimalField(
    max_digits=12,
    decimal_places=7,
    null=True,
    blank=True
)

    location = models.TextField(
        blank=True
    )


    out_at = models.DateTimeField(
        null=True,
        blank=True
    )

    out_image = models.ImageField(
        upload_to=attendance_out_image_path,
        blank=True,
        null=True
    )

    out_latitude = models.DecimalField(
        max_digits=12,
        decimal_places=7,
        null=True,
        blank=True
    )

    out_longitude = models.DecimalField(
        max_digits=12,
        decimal_places=7,
        null=True,
        blank=True
    )

    out_location = models.TextField(
        blank=True
    )

    

    camera = models.CharField(
        max_length=100,
        blank=True
    )

    confidence = models.FloatField(
        default=0
    )

    blink_verified = models.BooleanField(
        default=False
    )

    head_left = models.BooleanField(
        default=False
    )

    head_right = models.BooleanField(
        default=False
    )

    STATUS = (
        ("Present", "Present"),
        ("Late", "Late"),
        ("Absent", "Absent"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Present"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.date} - "
            f"{self.status}"
        )

class LeaveBalance(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="leave_balance"
    )

    cl = models.PositiveIntegerField(
        default=0
    )

    el = models.PositiveIntegerField(
        default=0
    )

    sl = models.PositiveIntegerField(
        default=0
    )

    total_leave = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.user.username} - Leave Balance"

class LoginLogoutLog(models.Model):

    ACTION_CHOICES = (
        ("Login", "Login"),
        ("Logout", "Logout"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_logout_logs"
    )

    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.action} - "
            f"{self.timestamp}"
        )




class LeaveApplication(models.Model):

    LEAVE_TYPES = (
        ("CL", "Casual Leave"),
        ("EL", "Earned Leave"),
        ("SL", "Sick Leave"),
    )

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leave_applications"
    )

    leave_type = models.CharField(
        max_length=2,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField(
        blank=True
    )

    days = models.PositiveIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.leave_type} - "
            f"{self.start_date} - "
            f"{self.status}"
        )



class ResignationApplication(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resignation_applications"
    )

    resignation_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.resignation_date} - "
            f"{self.status}"
        )