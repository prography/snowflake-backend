from django.core.files.images import ImageFile
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class UserTestCase(APITestCase):
    def test_create_user(self):
        url = reverse("accounts:user-list")
        data = {
            "email": "1@1.com",
            "password": "123",
            "username": "남바완",
            "image": ImageFile(open("media/1.png", "rb")),
            "social": "",
            "gender": 1,
            "partner_gender": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
