import base64
import re
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

"""
    Функция для изменения размеров входного изображения на указанные
    в данных тела входящего запроса
    
    Описание входных данных:
        data - входные данных изображения, отаправленные в теле входящего запроса
    
    Возвращаемый результат:
        Объект ContentFile (изменённое изображение)
"""


def resize_image(data):
    image_url = re.sub('^data:image/.+;base64,', '', data.get('image'))
    size = tuple(map(lambda x: data.get('image_size')[x], ['w', 'h']))
    image_format = data.get('save_format')

    buffer = BytesIO()
    new_image = Image.open(BytesIO(base64.b64decode(image_url))).resize(size)
    new_image.save(buffer, image_format)
    image_name = 'image-{0}.{1}'.format(data['id'][19:], image_format)
    return ContentFile(buffer.getvalue(), image_name)
