from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .modules.ImageResponse import create_response
from .modules.Validator import check_post_request
from .modules.TaskStatusCreator import create_task_status

from .tasks import image_resizing
from celery import uuid


class ResizeImageView(APIView):
    def get(self, request, pk):
        res = create_task_status(pk, image_resizing)

        if res is False:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    def post(self, request):
        errors = check_post_request(request.data)
        if len(errors) == 0:
            id_operation = uuid()
            res = image_resizing.apply_async((request.data, id_operation), task_id=id_operation)
            return Response(res.id, status=status.HTTP_201_CREATED)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class DownloadImageView(APIView):
    def get(self, request, pk):
        response = create_response(pk, status)
        return response
