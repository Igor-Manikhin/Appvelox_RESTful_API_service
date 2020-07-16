from rest_framework.views import APIView

from .modules.Responses import *


class ResizeImageView(APIView):
    # Обработчик входящих запросов на получение текущего статуса задачи
    def get(self, request, pk):
        return create_task_status_response(pk)

    # Обработчик входящих запросов на изменение размеров изображения
    def post(self, request):
        return create_post_response(request.data)


class DownloadImageView(APIView):
    # Обработчик входящих запросов на загрузку изменённых изображений
    def get(self, request, pk):
        return create_image_response(pk)
