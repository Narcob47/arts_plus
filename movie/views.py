# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from azure.storage.blob import BlobServiceClient
from django.conf import settings
import datetime

def get_video_url(blob_name):
    blob_service_client = BlobServiceClient(account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net", credential=settings.AZURE_ACCOUNT_KEY)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER_NAME, blob=blob_name)
    return blob_client.url

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        video_file = request.FILES.get('video_file')
        if not video_file:
            return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string("your_azure_connection_string")
        blob_client = blob_service_client.get_blob_client(container="your_container_name", blob=video_file.name)

        with video_file.open('rb') as data:
            blob_client.upload_blob(data)

        # Save video metadata to the database
        video = Video.objects.create(
            title=request.data.get('title'),
            description=request.data.get('description'),
            video_file=video_file.name
        )
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Generate a SAS URL for streaming
        blob_service_client = BlobServiceClient.from_connection_string("sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-02-04T16:01:15Z&st=2025-02-04T08:01:15Z&spr=https&sig=cAAv6SHZV3%2FssUPLDFCTMeUQuZElB%2BYUV3sxnVMesCY%3D")
        blob_client = blob_service_client.get_blob_client(container="studios", blob=instance.video_file)
        sas_url = blob_client.url + "?" + blob_client.generate_shared_access_signature(
            permission="r",
            expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        )

        return Response({"stream_url": sas_url}, status=status.HTTP_200_OK)