import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .modules.ImageResizer import ImageResize
from .modules.ImageResponse import ImageResponse

from .models import ResizeImages
from .serializers import ResizeImagesSerializer


class ResizeImageView(APIView):
    def get(self, request, pk):
        obj = ResizeImages.objects.get(pk=pk)
        data = ResizeImagesSerializer(obj).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        id_operation = uuid.uuid4()
        data['id'] = id_operation
        data['image'] = ImageResize.resize(data)
        data['image_status'] = 'Обработана'
        serializer = ResizeImagesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(id_operation, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DownloadImageView(APIView):
    def get(self, request, pk):
        image_data = ResizeImages.objects.values('image', 'save_format').get(pk=pk)
        response = ImageResponse.createResponse(image_data, status)
        return response
