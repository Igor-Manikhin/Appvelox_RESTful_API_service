import base64
import json
import os
from io import BytesIO
from uuid import UUID

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_FOLDER = os.path.join(CURRENT_DIR, 'test_data')

"""
    Функция для проверки идентификаторов изменённых изображений
    на корректность указания
    
    uuid - уникальный иденфификатор изменённого изображения в формате UUID4 
"""


def check_uuid(uuid):
    try:
        UUID(uuid, version=4)
    except ValueError:
        return False

    return True


class ResizeImageRequestsTests(APITestCase):
    """
        Тест для проверки корректности получаемых ответов для
        отправляемых в запросах на изменение размеров изображения
        корректных/некорректныых данных в формате JSON

        Тестовые данные расположены в файле resizing_images_test_data.txt

        Описание тестовых данных:

            incorrect_data - набор тестовых некорректных данных
            correct_data -  набор тестовых корректных данных
            incorrect_responses - набор ожидаемых ответы на запросы с указанными
                                  некорректными данными
            images_names - тестовые изображения, используемые в тестовом наборе
                           корректных данных
    """

    def test_resizing_images_correct_responses(self):
        url = reverse('Resize_Image')
        images_names = ['Image_1.JPG', 'Image_2.jpg', 'Image_3.JPG']
        download_url_template = "http://127.0.0.1:8000/api/v1/download/{}"
        result_url_template = 'http://127.0.0.1:8000/results/image-{0}.{1}'

        with open(TEST_DATA_FOLDER + "/resizing_images_test_data", 'r') as json_file:
            data = json.loads(json_file.read())

        for send_body, response_body in zip(data['incorrect_data'], data['incorrect_responses']):
            response = self.client.post(url, send_body, format='json')

            self.assertEqual(response.data, response_body)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for image_name, send_body in zip(images_names, data['correct_data']):
            img = Image.open(TEST_DATA_FOLDER + "/test_images/" + image_name)
            buffer = BytesIO()
            img.save(buffer, format=send_body['save_format'])
            send_body['image'] = b"data:image/jpeg;base64," + base64.b64encode(buffer.getvalue())

            response = self.client.post(url, send_body, format='json')
            self.assertEqual(check_uuid(response.data['task_id']), True)
            download_url = download_url_template.format(response.data['task_id'])
            result_url = result_url_template.format(response.data['task_id'][19:], send_body['save_format'])
            self.assertEqual(download_url, response.data['download_url'])
            self.assertEqual(result_url, response.data['result_url'])
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """
        Тест для проверки корректности получаемых ответов для отправляемых в
        запросах на получение текущего статуса задачи изменения изображения 
        корректных/некорректных и не существующих идентификаторов задач
        
        Тестовые данные расположены в файле get_tasks_statuses_test_data.txt
        
        Описание тестовых данных:
        
            incorrect_uuid - набор тестовых некорректных идентификаторов задач
            non_existing_uuid - набор тестовых не существующих идентификаторов задач
            existing_uuid - набор тестовых существующих идентификаторов задач
            incorrect_response - ожидаемый ответ на запрос с некорректным идентификатором задачи
            non_existing_response - ожидаемый ответ на запрос с не существующим идентификатором задачи
    """

    def test_task_statuses_correct_responses(self):

        with open(TEST_DATA_FOLDER + "/get_tasks_statuses_test_data", 'r') as json_file:
            data = json.loads(json_file.read())
            incorrect_response = bytes(data['incorrect_response'], encoding='utf-8')
            non_existing_response = bytes(data['non_existing_response'], encoding='utf-8')

        for task_id in data['incorrect_uuid']:
            url = reverse('Resize_Image_Status', kwargs={'pk': task_id})

            response = self.client.get(url)
            self.assertEqual(response.content, incorrect_response)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for task_id in data['non_existing_uuid']:
            url = reverse('Resize_Image_Status', kwargs={'pk': task_id})
            response = self.client.get(url)
            self.assertEqual(response.content, non_existing_response)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        for task_id, response_body in zip(data['existing_uuid'], data['correct_responses']):
            url = reverse('Resize_Image_Status', kwargs={'pk': task_id})
            response = self.client.get(url)
            self.assertEqual(response.data, response_body)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
        Тест для проверки корректности получаемых ответов для отправляемых
        в запросах на получение изменённых изображений корректных/некорректных
        и не существующих идентификаторов изменённых изображений
        
        Тестовые данные расположены в файле download_images_test_data.txt
        
        Описание тестовых данных:
        
            incorrect_uuid - набор тестовых некорректных идентификаторов изображений 
            non_existing_uuid - набор тестовых не существующих идентификаторов изображений
            existing_uuid - набор тестовых существующих идентификаторов изображений
            incorrect_response - ожидаемый ответ на запрос с некорректным идентификатором изображения
            non_existing_response - ожидаемый ответ на запрос с не существующим идентификатором изображения
    """

    def test_downloading_images_correct_responses(self):
        with open(TEST_DATA_FOLDER + "/download_images_test_data", 'r') as json_file:
            data = json.loads(json_file.read())
            incorrect_response = bytes(data['incorrect_response'], encoding='utf-8')
            non_existing_response = bytes(data['non_existing_response'], encoding='utf-8')

        for image_id in data['incorrect_uuid']:
            url = reverse('Download', kwargs={'pk': image_id})

            response = self.client.get(url)
            self.assertEqual(response.content, incorrect_response)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for image_id in data['non_existing_uuid']:
            url = reverse('Download', kwargs={'pk': image_id})

            response = self.client.get(url)
            self.assertEqual(response.content, non_existing_response)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        for image_id, resp_body in zip(data['existing_uuid'], data['correct_responses']):
            url = reverse('Download', kwargs={'pk': image_id})

            response = self.client.get(url)
            self.assertEqual(response['Content-Type'], resp_body['Content-Type'])
            self.assertEqual(response['Content-Disposition'], resp_body['Content-Disposition'])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
