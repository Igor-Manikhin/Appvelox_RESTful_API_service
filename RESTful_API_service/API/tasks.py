from __future__ import absolute_import, unicode_literals
from RESTful_API_service.celery import app
from .modules.ImageResizer import resize_image
from .serializers import ResizeImagesSerializer
from time import sleep


@app.task(bind=True, default_retry_delay=300, max_retries=5)
def image_resizing(self, post_data, operation_id):
    self.update_state(state='PROGRESS', meta={'test': 'test meta info'})
    sleep(60)
    data = post_data
    data['id'] = operation_id
    data['image'] = resize_image(data)
    data['image_status'] = 'Обработана'

    serializer = ResizeImagesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

