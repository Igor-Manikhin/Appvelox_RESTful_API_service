from rest_framework import serializers
from .models import ResizeImages


class ResizeImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResizeImages
        fields = '__all__'
