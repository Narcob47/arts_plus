from django.db import models
from movie.storage_backends import AzureMediaStorage

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    # Store only the HLS playlist (.m3u8) file
    hls_playlist = models.FileField(upload_to='hls/', storage=AzureMediaStorage(), blank=True, null=True)

    def __str__(self):
        return self.title

    def get_video_url(self):
        """Returns the HLS streaming URL if available"""
        if self.hls_playlist:
            return self.hls_playlist.url
        return None
