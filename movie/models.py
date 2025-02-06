from django.db import models
from movie.storage_backends import AzureMediaStorage

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/', storage=AzureMediaStorage())

    def __str__(self):
        return self.title

    def get_video_url(self):
        if self.video_file:
            return self.video_file.url
        return None