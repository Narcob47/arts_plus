from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from .utils.azure_upload import upload_to_azure_hls_files  # Import the upload function
import os

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        video_file = request.FILES.get('video_file')
        if not video_file:
            return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)

        local_video_folder = "C:/Users/Narco/Downloads/New_Video/"  # Local folder where the HLS files are saved

        file_urls = upload_to_azure_hls_files(local_video_folder)

        video = Video.objects.create(
            title=request.data.get('title'),
            description=request.data.get('description'),
            hls_playlist_url=file_urls.get("output.m3u8")  # Assuming your playlist file is named output.m3u8
        )

        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the specific video object
        video = self.get_object()

        # Check if the video has an HLS playlist URL
        if not video.hls_playlist_url:
            return Response({"error": "HLS playlist URL not found for this video"}, status=status.HTTP_404_NOT_FOUND)

        # Return the HLS streaming URL
        return Response({
            "title": video.title,
            "description": video.description,
            "hls_playlist_url": video.hls_playlist_url
        }, status=status.HTTP_200_OK)
