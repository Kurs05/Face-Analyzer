from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(default='default.png ', upload_to='avatars/')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    REQUIRED_FIELDS = ['email','password']

    def __str__(self):
        return self.username if self.username else 'No username'

class MediaFile(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='files')
    start_file = models.FileField()
    end_file = models.FileField(null=True, blank=True)
    landmarks_file = models.FileField(null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file_name = models.CharField(max_length=120)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.file_name} ({self.file_type})"

class DetectedFace(models.Model):
    media = models.ForeignKey(MediaFile, on_delete=models.CASCADE, related_name='faces')
    timestamp = models.FloatField(null=True, blank=True)  # Для видео (в секундах), null для изображений
    name = models.CharField(max_length=120)
    data = models.JSONField()

    def __str__(self):
        return f"Face in {self.media.file_name} @ {self.name}"

class Emotion(models.Model):
    face = models.ForeignKey(DetectedFace, on_delete=models.CASCADE, related_name='emotions')
    type = models.CharField(max_length=20)  # например: 'HAPPY', 'SAD', ...
    confidence = models.FloatField()

    def __str__(self):
        return f"{self.face} {self.type} ({self.confidence:.2f}%)"


