# models.py
from django.db import models
from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from movie.storage_backends import AzureMediaStorage

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/', storage=AzureMediaStorage())

    def __str__(self):
        return self.title