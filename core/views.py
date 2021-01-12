from rest_framework import APIView

from api import serializers
from api import models


class TaskApiView(APIView):
    serializer_class = serializers.TaskSerializer

    def get(self, request):
        