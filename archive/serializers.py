from rest_framework import serializers
from core import models


class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Archive
        fields = ['id', 'name', 'info', 'user']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = [
            'id', 'original_name', 'image_source',
            'info', 'image', 'archive']
        extra_kwargs = {
            'id': {'read_only': True},
            'image': {'read_only': True},
            'archive': {'read_only': True},
        }


class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('id', 'image')
        extra_kwargs = {
            'id': {'read_only': True},
            'image': {'required': True}
        }
