from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from celery import uuid
from PIL import Image

from ..serializers import ResizeImagesSerializer
from ..models import ResizeImages
from ..tasks import image_resizing
from .Validator import *


def create_post_response(data):
    base_url = 'http://127.0.0.1:8000/api/v1/download/'
    response_data = dict()

    errors = check_post_request(data)
    if len(errors) == 0:
        task_id = uuid()
        image_resizing.apply_async(args=(data, task_id), task_id=task_id)
        response_data['task_id'] = task_id
        response_data['download_url'] = base_url + task_id
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def create_task_status_response(task_id):

    if check_get_uuid(task_id) is False:
        return HttpResponse("400 BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    info = dict()
    res = AsyncResult(task_id, task_name=image_resizing)

    if res.state == 'PENDING':
        return HttpResponse("404 NOT FOUND", status=status.HTTP_404_NOT_FOUND)

    info['status'] = res.state
    info['status_info'] = res.info

    return Response(info, status=status.HTTP_200_OK)


def create_image_response(image_id):

    if check_get_uuid(image_id) is False:
        return HttpResponse("400 BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    image_data = ResizeImages.objects.filter(pk=image_id).values('image', 'save_format')

    if len(image_data) == 0:
        return HttpResponse("404 NOT FOUND", status=status.HTTP_404_NOT_FOUND)

    file_path = 'results/{0}'.format(image_data[0].get('image'))
    file = Image.open(file_path)
    mime_type = 'image/{0}'.format(image_data[0].get('save_format'))
    response = HttpResponse(content_type=mime_type, status=status.HTTP_200_OK)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(image_data[0].get('image'))
    file.save(response, image_data[0].get('save_format'))

    return response
