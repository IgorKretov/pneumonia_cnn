from rest_framework import serializers
from core import models
from tf_model.model_serving import process_image, predict
from app.settings import BASE_DIR, CNN_MODEL_PATH


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
            'id', 'name', 'info', 'image',
            'predicted_class', 'predicted_value', 'archive'
        ]
        read_only_fields = [
            'id', 'image', 'archive',
            'predicted_class', 'predicted_value'
        ]


class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('id', 'image')
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ImagePredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('id', 'predicted_class', 'predicted_value')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def update(self, instance, validated_data):
        image_path = BASE_DIR + instance.image.url.replace('/', '\\')
        image_array = process_image(image_path)
        predicted_class, predicted_value = predict(CNN_MODEL_PATH, image_array)
        validated_data['predicted_class'] = predicted_class
        validated_data['predicted_value'] = predicted_value
        return super().update(instance, validated_data)
