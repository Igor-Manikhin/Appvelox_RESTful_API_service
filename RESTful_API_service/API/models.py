from django.contrib.postgres.fields import JSONField
from django.db import models


class ResizeImages(models.Model):
    id = models.UUIDField(primary_key=True)
    image = models.ImageField()
    image_size = JSONField()
    save_format = models.CharField(max_length=4)
    image_status = models.CharField(max_length=20)
