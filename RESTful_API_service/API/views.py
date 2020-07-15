from rest_framework.views import APIView
from .modules.Responses import *


class ResizeImageView(APIView):
    def get(self, request, pk):
        return create_task_status_response(pk)

    def post(self, request):
        return create_post_response(request.data)


class DownloadImageView(APIView):
    def get(self, request, pk):
        return create_image_response(pk)
