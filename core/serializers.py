from rest_framework import serializers
from api import models


class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Task
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = '__all__'
        extra_kwargs = {
            'task': {'read_only': True}
        }