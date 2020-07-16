from PIL import Image
from celery import uuid
from celery.result import AsyncResult
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from .Validator import *
from ..models import ResizeImages
from ..tasks import image_resizing

"""
    Функция для создания ответа на входящий запрос на изменение размеров изображения

    Описание входных данных:
        data - входные данных изображения, отаправленные в теле входящего запроса
    
    Возращаемый результат:
        errors (если были указаны некорректные данные в теле входящего запроса)
        response_data (если были указаны корректные данные в теле входящего запроса)
    
    Описание response data:
        task_id - уникальный идентификатор статуса задачи на изменение размеров изображения
        result_url - ссылка для предварительного просмотра изменённого изображения
        download_url - ссылка для скачивания изменённого изображения 
"""


def create_post_response(data):
    download_url_template = 'http://127.0.0.1:8000/api/v1/download/{}'
    result_url_template = 'http://127.0.0.1:8000/results/image-{0}.{1}'
    response_data = dict()

    errors = check_post_request(data)
    if len(errors) == 0:
        task_id = uuid()
        image_resizing.apply_async(args=(data, task_id), task_id=task_id)
        response_data['task_id'] = task_id
        response_data['result_url'] = result_url_template.format(task_id[19:], data['save_format'])
        response_data['download_url'] = download_url_template.format(task_id)
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


"""
    Функция для создания ответа на входящий запрос на получение текущего статуса задачи
    изменения размеров изображения
    
    Описание входных данных:
        task_id - идентификатор задачи
    
    Возращаемый результат:
        400 BAD REQUEST (если идентификатор задачи был указан некорректно)
        404 NOT FOUND (если задачи с таким идентификатором не существует)
        info (если идентификатор задачи был указан корректно)
    
    Описание current_task_info
        status - текущий статус задачи
        status_info - подробное описание статуса задачи (зависит от текущего статуса) 
"""


def create_task_status_response(task_id):
    if check_get_uuid(task_id) is False:
        return HttpResponse("400 BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    res = AsyncResult(task_id, task_name=image_resizing)

    if res.state == 'PENDING':
        return HttpResponse("404 NOT FOUND", status=status.HTTP_404_NOT_FOUND)

    current_task_info = dict(status=res.state, status_info=res.info)

    return Response(current_task_info, status=status.HTTP_200_OK)


"""
    Функция для создания ответа на входящий запрос на загрузку изменённого
    изображения
    
    Описание входных данных:
        task_id - идентификатор изменённого изображения
    
    Возращаемый результат:
        400 BAD REQUEST (если идентификатор изображения был указан некорректно)
        404 NOT FOUND (если изображения с таким идентификатором не существует)
        image (если идентификатор изображения был указан корректно)
"""


def create_image_response(image_id):
    if check_get_uuid(image_id) is False:
        return HttpResponse("400 BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    image_data = ResizeImages.objects.filter(pk=image_id).values('image', 'save_format')

    if len(image_data) == 0:
        return HttpResponse("404 NOT FOUND", status=status.HTTP_404_NOT_FOUND)

    image_path = 'results/{0}'.format(image_data[0]['image'])
    image = Image.open(image_path)
    mime_type = 'image/{0}'.format(image_data[0]['save_format'])
    response = HttpResponse(content_type=mime_type, status=status.HTTP_200_OK)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(image_data[0]['image'])
    image.save(response, image_data[0]['save_format'])

    return response
