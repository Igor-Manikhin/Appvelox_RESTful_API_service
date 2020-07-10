from django.urls import path
from .views import ResizeImageView

urlpatterns = [
    path('statusImage/<str:pk>', ResizeImageView.as_view(), name='Resize_Image_Status'),
    path('resizeImage', ResizeImageView.as_view(), name='Resize_Image'),
]