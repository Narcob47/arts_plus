# Generated by Django 5.1.5 on 2025-02-06 15:01

import movie.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_video_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_file',
        ),
        migrations.AddField(
            model_name='video',
            name='hls_playlist',
            field=models.FileField(blank=True, null=True, storage=movie.storage_backends.AzureMediaStorage(), upload_to='hls/'),
        ),
    ]
