from rest_framework import serializers
from .models import ResizeImages


class ResizeImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResizeImages
        fields = ['id', 'image', 'image_size', 'save_format', 'image_status']