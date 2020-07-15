import json
import os

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_FOLDER = os.path.join(CURRENT_DIR, 'test_data')


class ResizeImageRequestsTests(APITestCase):
    def test_correct_data(self):
        url = reverse('Resize_Image')

        with open(TEST_DATA_FOLDER + "/post_test_data", 'r') as json_file:
            data = json.loads(json_file.read())

        for send_body, response_body in zip(data['incorrect_data'], data['response_data']):
            response = self.client.post(url, send_body, format='json')
            self.assertEqual(response.data, response_body)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_status_task(self):

        with open(TEST_DATA_FOLDER + "/get_task_status_test_data", 'r') as json_file:
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

    def test_download_image(self):
        with open(TEST_DATA_FOLDER + "/download_image_test_data", 'r') as json_file:
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
