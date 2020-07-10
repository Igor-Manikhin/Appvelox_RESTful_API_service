import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .modules.ImageResizer import ImageResize

from .models import ResizeImages
from .serializers import ResizeImagesSerializer


class ResizeImageView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(ResizeImages, pk=pk)
        data = ResizeImagesSerializer(obj).data
        return Response(data)

    def post(self, request):
        data = request.data
        data['id'] = uuid.uuid4()
        data['image'] = ImageResize.resize(data)
        data['image_status'] = 'Обработана'
        serializer = ResizeImagesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("успех", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
