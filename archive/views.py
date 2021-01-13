from core.models import Archive, Image
from archive.serializers import ArchiveSerializer, ImageSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import views, status, generics


class ArchiveList(generics.ListCreateAPIView):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


class ArchiveDetail(views.APIView):
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
        serializer = ArchiveSerializer(archive, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        archive = self.get_one(id)
        archive.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageDetail(views.APIView):
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
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        image = self.get_one(id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
