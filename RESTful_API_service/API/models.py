from django.contrib.postgres.fields import JSONField
from django.db import models

"""
    Модель таблицы ResizeImages в базе данных для хранения информациии по изменённым изображениям
    
    Описание полей модели таблицы:
        id - уникальный идентификатор изображения
        image - путь хранения изображения в медиа директории
        image_size - размеры изображения (высота и ширина)
        save_format - формат, в котором было сохранено изображение
"""


class ResizeImages(models.Model):
    id = models.UUIDField(primary_key=True)
    image = models.ImageField()
    image_size = JSONField()
    save_format = models.CharField(max_length=4)
