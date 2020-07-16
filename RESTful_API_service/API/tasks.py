from __future__ import absolute_import, unicode_literals

from time import sleep, time

from celery import states

from RESTful_API_service.celery import app
from .modules.ImageResizer import resize_image
from .serializers import ResizeImagesSerializer

started_meta = {'description': 'Run task started'}
progress_meta_1 = {'description': 'Task in progress', 'Performed': '35%'}
progress_meta_2 = {'description': 'Task in progress', 'Performed': '75%'}
finish_meta = {'description': 'Task completed'}

"""
    Задача на изменение размера изображения на указанные
    в данных тела входящего запроса
    
    Для демонстрации работоспособности асинхронности и возможности просмотра
    прожемуточных статусов поставленной задачи - была искусстренно
    установленна задержка в 80 секунд. 
    
    Описание входных данных:
        request_data - входные данных изображения, отаправленные в теле входящего запроса
        task_id - присваиваемый задаче уникальный идентификатор
    
    Возвращаемый результат:
        finish_meta - информация по статусу успешного выполнения задачи
    
    Описание finish_meta:
         time_spend - затраченное время на выполнение задачи
"""


@app.task(bind=True, default_retry_delay=300, max_retries=5)
def image_resizing(self, request_data, task_id):
    data = request_data
    start_time = time()
    self.update_state(state=states.STARTED, meta=started_meta)
    sleep(20)
    data['id'] = task_id
    self.update_state(state='PROGRESS', meta=progress_meta_1)
    sleep(30)
    data['image'] = resize_image(data)
    self.update_state(state='PROGRESS', meta=progress_meta_2)
    sleep(30)
    serializer = ResizeImagesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        finish_meta['time_spent'] = str("{} seconds".format(time() - start_time))

        return finish_meta
