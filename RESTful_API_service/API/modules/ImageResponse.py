from django.http import HttpResponse
from ..models import ResizeImages
from .Validator import check_get_uuid
from PIL import Image


def create_response(image_id, status):
    valid_uuid = check_get_uuid(image_id)

    if valid_uuid is False:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    image_data = ResizeImages.objects.filter(pk=image_id).values('image', 'save_format')

    if len(image_data) == 0:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    file_path = 'downloads/{0}'.format(image_data[0].get('image'))
    file = Image.open(file_path)
    mime_type = 'image/{0}'.format(image_data[0].get('save_format'))
    response = HttpResponse(content_type=mime_type, status=status.HTTP_200_OK)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(image_data[0].get('image'))
    file.save(response, image_data[0].get('save_format'))

    return response
