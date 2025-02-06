from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import datetime
import base64
from movie.storage_backends import AzureMediaStorage  # ✅ Fixed import

account_key_bytes = base64.b64decode(AzureMediaStorage.account_key)

# Function to generate a signed URL for streaming
def get_video_url(blob_name):
    if not blob_name:  # ✅ Prevent invalid file names
        raise ValueError("Invalid blob name: Blob name cannot be empty.")

    sas_token = generate_blob_sas(
    account_name=AzureMediaStorage.account_name,
    container_name=AzureMediaStorage.azure_container,
    blob_name=blob_name,
    account_key=account_key_bytes,  # ✅ Fix: Ensure it's bytes
    permission=BlobSasPermissions(read=True),
    expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
)

    blob_url = f"https://{AzureMediaStorage.account_name}.blob.core.windows.net/{AzureMediaStorage.azure_container}/{blob_name}?{sas_token}"
    return blob_url

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        video_file = request.FILES.get('video_file')
        if not video_file:
            return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(AzureMediaStorage.connection_string)
        blob_client = blob_service_client.get_blob_client(container=AzureMediaStorage.azure_container, blob=video_file.name)

        with video_file.open('rb') as data:
            blob_client.upload_blob(data, overwrite=True)  # ✅ Allows overwriting existing files

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

        if not instance.video_file:  # ✅ Prevents errors if filename is missing
            return Response({"error": "Video file not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the URL from the FileField
        stream_url = instance.video_file.url  

        return Response({"stream_url": stream_url}, status=status.HTTP_200_OK)
