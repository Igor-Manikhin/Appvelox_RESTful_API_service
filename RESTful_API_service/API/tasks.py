from __future__ import absolute_import, unicode_literals
from celery import current_task, shared_task, states
from .modules.ImageResizer import resize_image
from .serializers import ResizeImagesSerializer
from time import sleep, time

started_meta = {'description': 'Run task started'}
progress_meta_1 = {'description': 'Task in progress', 'Performed': '35%'}
progress_meta_2 = {'description': 'Task in progress', 'Performed': '75%'}
finish_meta = {'description': 'Task completed'}


@shared_task
def image_resizing(post_data, task_id):
    start_time = time()
    current_task.update_state(state=states.STARTED, meta=started_meta)
    sleep(20)
    data = post_data
    data['id'] = task_id
    current_task.update_state(state='PROGRESS', meta=progress_meta_1)
    sleep(30)
    data['image'] = resize_image(data)
    data['image_status'] = 'Обработана'
    current_task.update_state(state='PROGRESS', meta=progress_meta_2)
    sleep(30)
    serializer = ResizeImagesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        finish_meta['Time spent'] = str("{} seconds".format(time() - start_time))

        return finish_meta
