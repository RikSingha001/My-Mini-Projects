from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

class DataAnalysisWithWeb(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    file = models.FileField(
        upload_to='data_analysis_files/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"