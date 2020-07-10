from django.http import HttpResponse
from PIL import Image


class ImageResponse:
    @staticmethod
    def createResponse(data, status):
        image_name = data.get('image')
        image_format = data.get('save_format')

        filepath = 'downloads/{0}'.format(image_name)
        file = Image.open(filepath)
        mime_type = 'image/{0}'.format(image_format)
        response = HttpResponse(content_type=mime_type, status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'attachment; filename={0}'.format(image_name)
        file.save(response, image_format)
        return response
