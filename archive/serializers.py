from rest_framework import serializers
from core import models


class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Archive
        fields = ['id', 'name', 'info']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = [
            'id', 'original_name', 'info',
            'saved_name', 'saved_path', 'archive'
        ]
        extra_kwargs = {
            'archive': {'read_only': True}
        }
