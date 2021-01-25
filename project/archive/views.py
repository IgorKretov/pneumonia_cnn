from core.models import Archive, Image
from archive.serializers import ArchiveSerializer, ImageSerializer, \
                                ImageUploadSerializer, \
                                ImagePredictionSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import views, status, viewsets, generics


class ArchiveList(generics.ListCreateAPIView):
    """APIView for creating an archive
    or listing archives which belong to a user
    """
    serializer_class = ArchiveSerializer

    def get_queryset(self):
        return Archive.objects.filter(user=self.request.user).order_by('id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArchiveDetail(views.APIView):
    """APIView for archive detail
    This has get, update, and delete functions for an archive.
    """
    def get_one(self, id):
        try:
            return Archive.objects.get(pk=id)
        except Archive.DoesNotExist:
            raise Http404

    def get(self, request, id):
        archive = self.get_one(id)
        serializer = ArchiveSerializer(archive)
        return Response(serializer.data)

    def put(self, request, id):
        archive = self.get_one(id)
        serializer = ArchiveSerializer(
            archive,
            data=request.data,
            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        archive = self.get_one(id)
        archive.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageList(generics.ListCreateAPIView):
    """APIView for creating an Image
    or listing images which belong to an archive
    """
    serializer_class = ImageSerializer

    def get_queryset(self):
        archive = Archive.objects.get(pk=self.kwargs['archive_id'])
        return Image.objects.filter(archive=archive).order_by('id')

    def perform_create(self, serializer):
        archive = Archive.objects.get(pk=self.kwargs['archive_id'])
        serializer.save(archive=archive)


class ImageDetail(views.APIView):
    """APIView for image detail
    This has get, update, and delete functions for an image.
    """
    def get_one(self, id):
        try:
            return Image.objects.get(pk=id)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, id):
        image = self.get_one(id)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, id):
        image = self.get_one(id)
        serializer = ImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        image_instance = self.get_one(id)
        image_instance.image.delete()
        image_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageUploadViewSet(viewsets.ViewSet):
    """ViewSet for uploading an image file
    Uploaded image becomes a ImageField of an image instance.
    """
    serializer_class = ImageUploadSerializer

    def update(self, request, id):
        image_instance = Image.objects.get(pk=id)
        serializer = self.serializer_class(image_instance, data=request.data)
        if serializer.is_valid():
            if image_instance.image:
                image_instance.image.delete()
                image_instance.predicted_class = None
                image_instance.predicted_value = None
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImagePredictionViewSet(viewsets.ViewSet):
    """Viewset for predicting the probability of pneumonia for a given image
    Predicted class and predicted value become fields of an image instance.
    """
    serializer_class = ImagePredictionSerializer

    def update(self, request, id):
        image = Image.objects.get(pk=id)
        serializer = self.serializer_class(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
